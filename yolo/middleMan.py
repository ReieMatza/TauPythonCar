import queue
from classes import Detection
from sympy import symbols, Eq, solve
import math
import MapApi
import os
from RAndTMatrix import *


def getPosEstimation(distance, dgrees, camPosition):
    d = distance
    tanO = math.tan((90-dgrees)*math.pi/180)
    xp = camPosition[0]
    yp = camPosition[1]
    x, y = symbols('x y')

    eq1 = Eq((xp -x)*(xp -x) +(yp-y)*(yp-y) - d*d, 0)
    eq2 = Eq((yp-y) -tanO*(xp -x), 0)
    sol = solve((eq1,eq2), (x, y))
    sol1 = sol[0]
    sol2 = sol[1]
    print(sol)
    #print("check    ---------------------> " + str(dgrees))
    if dgrees > 90 and dgrees < -90:
        if sol1[1] < yp:
            sol = sol1
        else:
            sol = sol2
    if dgrees < 90 and dgrees > -90:
        if sol1[1] > yp:
            sol = sol1
        else:
            sol = sol2

    return sol


def detectionsQueueLoop(detectionsQueue,trackMap):
    
    
    while (True):
        if detectionsQueue.empty() == False:
            detection = detectionsQueue.get()
            
            if abs(detection.camDistance - float(detection.depthDistance)) < 0.8 and detection.camDistance < 11 and detection.camDistance > 2 and abs(detection.relHeading) < 32 and abs(detection.relHeading + detection.camOrientation[2]) > 7:
                estimatedPos = getPosEstimation(detection.camDistance, detection.relHeading + detection.camOrientation[2], detection.camPosition)
                #print("coneColor: " + detection.coneColor +" camDistance: " + str(detection.camDistance) + " depthDistance: " + str(detection.depthDistance) + " relHeading: " + str(detection.relHeading)+ " camPosition: " + str(detection.camPosition) + " camOrientation: " + str(detection.camOrientation))
                with open('detectionsOutput.txt', 'a') as file:
                    file.write(str(detection.coneColor) + "\t" + str(detection.camDistance) + "\t" + str(detection.depthDistance) + "\t" + str(detection.relHeading)+ "\t" + str(detection.camPosition[0]) + "\t" + str(detection.camPosition[1]) + "\t" + str(detection.camPosition[2]) + "\t" + str(detection.camOrientation[0]) + "\t" + str(detection.camOrientation[1]) + "\t" + str(detection.camOrientation[2]) + "\t" + str(detection.frameID) + "\n")
                #detection.coneColor    #accepts BLUE/YELLOW as values
                # y_cord = estimatedPos[1]
                # x_cord = estimatedPos[0]
                # Matza addCone here
                #print('Before: ' + str(detection.coneColor) + ' ' + str(estimatedPos[0]) +' ' + str(estimatedPos[1]))
                trackMap.addCone(estimatedPos[0],estimatedPos[1],detection.coneColor)
