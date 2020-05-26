from operator import add , sub
import csv
import queue

class unixTime:
    def __init__(self,unixTime,timeMicrosecons):
        self.unixTime = unixTime
        self.timeMicrosecons = timeMicrosecons

class Cone:
# Cone type to create a list of cones from
    def __init__(self, distance = None, heading = None, coneType = None):
        self.destance = distance
        self.heading = heading
        self.coneType = coneType

class CarStatus:
    # this class goes in the que a better name for it would be CarStatueUpdate
    # uptadeTypes 1: location update ,2: heading update ,3: cone list update, 4:time update
    def __init__(self, heading = 0 , x = 0 ,y = 0,z = 0, uptadeType = None, coneList = None,unixTime = 0,timeMicrosecons = 0):
        self.heading = heading 
        self.location = [x,y,z]
        self.type = uptadeType
        self.coneList = coneList
        self.unixTime = unixTime
        self.timeMicrosecons = timeMicrosecons


class Car:
    #Any data that is currently corrent for the car for example the list of cones after the SLAM
    def __init__(self, heading = 0 , x = 0 ,y = 0,z = 0, timeUnix = 0, timeMicrosecons = 0):
        self.heading = heading 
        self.zeroLocaion = [x,y,z]
        self.zeroHeading = heading
        self.location = [0,0,0]
        self.timeUnix = timeUnix
        self.timeMicrosecons = timeMicrosecons
        self.timeQueue = queue.Queue()
        

    def updateStatus(self, carStatus,plotFile,fieldnames):
        if carStatus.type == 1:
            self.location = list(map(sub,carStatus.location, self.zeroLocaion))
            with open(plotFile, 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                info = {"Northing (m)": self.location[0],"Easting (m)": self.location[1]}
                csv_writer.writerow(info)
        elif carStatus.type == 2:
            self.heading = ((carStatus.heading-self.zeroHeading)+360)%360
        elif carStatus.type == 3:
            self.timeMicrosecons = carStatus.timeMicrosecons
            self.timeUnix = carStatus.unixTime
            with self.timeQueue.mutex:
                self.timeQueue.queue.clear()
            self.timeQueue.put(unixTime(self.timeUnix,self.timeMicrosecons))

# sets the zero time of the system
    def updateTime(self, newTime):
        self.time = newTime

# sets the zero loaction of the system
    def setZero(self,location):
        self.zeroLocaion = location
        self.location = [0,0,0]

#sets the zero heading of the system
    def setZeroHeading(self,heading):
        self.zeroHeading = heading
        

