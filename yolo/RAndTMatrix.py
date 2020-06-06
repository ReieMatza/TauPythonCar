import math
import numpy as np



def CreateInverseRotionMatrix(theta):
    thataInRad = math.radians(theta)
    rotationMatrix = np.zeros((2,2))
    rotationMatrix[0,0] = math.cos(thataInRad)
    rotationMatrix[1,0] = -1 * math.sin(thataInRad)
    rotationMatrix[0,1] = math.sin(thataInRad)
    rotationMatrix[1,1] = math.cos(thataInRad)
    return rotationMatrix

def InverseTranslation(pointX,pointY,carLocationX,carLocationY):
    pointX = pointX - carLocationX
    pointX = pointY - carLocationY
    return pointX,pointY 

def GetAbsoluteLocation(pointX,pointY,carLocationX,carLocationY,carHeading):
    absLocation = np.zeros((2,1))
    absLocation[0],absLocation[1] =InverseTranslation(pointX,pointY,carLocationX,carLocationY)
    absLocation = (np.CreateInverseRotionMatrix(carHeading),absLocation)
    return absLocation

def DetectionToAbsLocation(detection):
    coneX= math.cos(detection.relHeading)* detection.camDistance
    coneY= math.sin(detection.relHeading)* detection.camDistance
    absLocation = GetAbsoluteLocation(coneX,coneY,detection.camPosition[0],detection.camPosition[1],detection.camOrientation[2])
    return absLocation
