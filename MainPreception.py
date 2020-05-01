import sys
import csv
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

def main():
    saveDataFile = 'data.csv'
    fieldnames = ["x_value", "y_value"]


    with open(saveDataFile, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    carStatueQueue = queue.Queue()
    imuThread = threading.Thread(target = ImuLoop, args =(carStatueQueue,'data.csv',fieldnames,), daemon=True)
    imuThread.start()
    car = Car()

    SLAM.RunSLAM(car,carStatueQueue,saveDataFile,fieldnames)


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