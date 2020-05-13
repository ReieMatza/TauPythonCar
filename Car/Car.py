from operator import add , sub
import csv

class Cone:
# Cone type to create a list of cones from
    def __init__(self, distance = None, heading = None, coneType = None):
        self.destance = distance
        self.heading = heading
        self.coneType = coneType

class CarStatus:
    # this class goes in the que a better name for it would be CarStatueUpdate
    # uptadeTypes 1: location update ,2: heading update ,3: cone list update
    def __init__(self, heading = 0 , x = 0 ,y = 0,z = 0, uptadeType = None, coneList = None):
        self.heading = heading 
        self.location = [x,y,z]
        self.type = uptadeType
        self.coneList = coneList


class Car:
    #Any data that is currently corrent for the car for example the list of cones after the SLAM
    def __init__(self, heading = 0 , x = 0 ,y = 0,z = 0, timeSeconds = 0, timeMilisecons = 0):
        self.heading = heading 
        self.zeroLocaion = [x,y,z]
        self.zeroHeading = heading
        self.location = [0,0,0]
        self.timeSeconds = timeSeconds
        self.timeMilisecons = timeMilisecons

    def updateStatus(self, carStatus,plotFile,fieldnames):
        if carStatus.type == 1:
            self.location = list(map(sub,carStatus.location, self.zeroLocaion))
            with open(plotFile, 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                info = {"Northing (m)": self.location[0],"Easting (m)": self.location[1]}
                csv_writer.writerow(info)
        elif carStatus == 2:
            self.heading = carStatus.heading

    def updateTime(self, newTime):
        self.time = newTime

    def setZero(self,location):
        self.zeroLocaion = location
        self.location = [0,0,0]
    def setZeroHeading(self,heading):
        self.zeroHeading = heading
        

