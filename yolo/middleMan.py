import queue
from classes import Detection
from sympy import symbols, Eq, solve
import math
import MapApi
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

conesList = []
initBlueConesListX = []
initBlueConesListY = []
initYellowConesListX = []
initYellowConesListY = []


def CameraRotationCompnsation(pointX,pointY,theta):
    thataInRad = 1*math.radians(theta)
    rotationMatrix = np.zeros(2)
    rotationMatrix[0] = pointX*math.cos(thataInRad)-pointY*math.sin(thataInRad)
    rotationMatrix[1] = pointX*math.sin(thataInRad)+pointY*math.cos(thataInRad)
    return rotationMatrix

def InverseTranslation(pointX,pointY,carLocationX,carLocationY):
    pointX = pointX + carLocationX
    pointY = pointY + carLocationY
    return pointX,pointY 

def GetAbsoluteLocation(pointX,pointY,carLocationX,carLocationY,carHeading):
    absLocation = np.zeros((2,1))
    absLocation[0] = pointX
    absLocation[1] = pointY
    absLocation = CameraRotationCompnsation(pointX,pointY,carHeading)
    absLocation[0],absLocation[1] =InverseTranslation(absLocation[0],absLocation[1],carLocationX,carLocationY)
    
    return absLocation

def DetectionToAbsLocation(detection):
    coneX= math.sin(math.radians(detection.relHeading)) * float(detection.depthDistance)
    coneY= math.cos(math.radians(detection.relHeading)) * float(detection.depthDistance)
    absLocation = GetAbsoluteLocation(coneX,coneY,detection.camPosition[0],detection.camPosition[1],detection.camOrientation[2])
    return (absLocation[0],absLocation[1])

def detectionsQueueLoop(detectionsQueue,trackMap):
    blueConesK = 2
    yellowConesK = 2
    i = 1
    while (True):

        if detectionsQueue.empty() == False:
            detection = detectionsQueue.get()
            if abs(detection.camDistance - float(detection.depthDistance)) < 3 and detection.camDistance < 18 and detection.camDistance > 0.5 and abs(detection.relHeading) < 46.25 and abs(detection.relHeading) > 0.05:
            # if  1:
                
                estimatedPos = DetectionToAbsLocation(detection)
                if detection.coneColor == "BLUE":
                    initBlueConesListX.append(estimatedPos[0])
                    initBlueConesListY.append(estimatedPos[1])
                elif detection.coneColor == "YELLOW":
                    initYellowConesListX.append(estimatedPos[0])
                    initYellowConesListY.append(estimatedPos[1])
                #conesList.append(estimatedPos[0], estimatedPos[1], detection.color)
                with open('cordsOutput.txt', 'a') as file:
                     file.write(detection.coneColor + "\t" + str(estimatedPos[0]) + "\t" + str(estimatedPos[1]) + "\n")
                if i % 20 == 0:
                    blueConesK, yellowConesK = kmeansEstimation(blueConesK, yellowConesK)
                    trackMap.updateConeList(conesList)
                    i = 1
                i += 1

def kmeansEstimation(blueConesK, yellowConesK):
    sil = []

    
    if len(initBlueConesListX) > 10:
        df = pd.DataFrame({'x': initBlueConesListX, 'y': initBlueConesListY}) 

        blueConesK -= 3
        if blueConesK < 2:
            blueConesK = 2

        for i in range(blueConesK,blueConesK+6):
            kmeans = KMeans(n_clusters=i , max_iter = 600)
            kmeans.fit(df)
            labels = kmeans.predict(df)
            centroids = kmeans.cluster_centers_
            sil.append(silhouette_score(df, labels, metric = 'euclidean'))
        

        blueConesK = range(blueConesK,blueConesK + 6)[sil.index(max(sil))]

        kmeans = KMeans(n_clusters=blueConesK ,max_iter = 600)
        kmeans.fit(df)
        labels = kmeans.predict(df)
        centroids = kmeans.cluster_centers_

        for centroid in centroids:
            conesList.append((centroid[0],centroid[1], "BLUE"))

        sil.clear()
    if len(initYellowConesListX) > 10:    
        df = pd.DataFrame({'x': initYellowConesListX, 'y': initYellowConesListY}) 
    
        yellowConesK -= 3
        if yellowConesK < 2:
            yellowConesK = 2

        for i in range(yellowConesK,yellowConesK+6):
            kmeans = KMeans(n_clusters=i , max_iter = 600)
            kmeans.fit(df)
            labels = kmeans.predict(df)
            centroids = kmeans.cluster_centers_
            sil.append(silhouette_score(df, labels, metric = 'euclidean'))
        
        yellowConesK = range(yellowConesK,yellowConesK + 6)[sil.index(max(sil))]



        kmeans = KMeans(n_clusters=yellowConesK , max_iter = 600)
        kmeans.fit(df)
        labels = kmeans.predict(df)
        centroids = kmeans.cluster_centers_

        for centroid in centroids:
            conesList.append((centroid[0],centroid[1], "YELLOW"))
    return blueConesK, yellowConesK