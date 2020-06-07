import math
import numpy as np
from classes import Detection



def CameraRotationCompnsation(pointX,pointY,theta):
    thataInRad = -1*math.radians(theta)
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
    coneX= math.sin(math.radians(detection.relHeading))* detection.camDistance
    coneY= math.cos(math.radians(detection.relHeading))* detection.camDistance
    absLocation = GetAbsoluteLocation(coneX,coneY,detection.camPosition[0],detection.camPosition[1],detection.camOrientation[2])
    return (absLocation[0],absLocation[1])