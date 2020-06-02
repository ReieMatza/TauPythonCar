import sys
import time
import os
import queue
import threading
import matplotlib.pyplot as plt

dir = os.path.dirname(__file__)
IMUpath = os.path.join(dir, 'IMU')
CARpath = os.path.join(dir, 'Car')
sys.path.append(IMUpath)
sys.path.append(CARpath)

from Car import *
from IMUPython import *
import SLAM
from MapApi import *

class OppMode:
    def __init__(self, type = "online", path = ""):
        self.type = type
        self.path = path

def main():

    trackMap = TrackMap()
    carStatueUpdateQueue = queue.Queue()
    imuThread = threading.Thread(target = ImuLoop, args =(carStatueUpdateQueue,'data.csv',trackMap,), daemon=True)
    imuThread.start()
    car = Car()
    # oppMode = OppMode(type = 'offline',path = 'C:\\FinalProject\\TauPythonCar\\UTMPosition.csv')
    oppMode = OppMode("online")
    
    SLAM.RunSLAM(car,carStatueUpdateQueue,trackMap,oppMode)


    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # fig.show()
    # ax.relim() 
    # ax.autoscale_view(True,True,True)
    # fig.canvas.draw()
    # plt.show(block=False)
    # pltData = []

    

            
        

if __name__ == "__main__":
    main()