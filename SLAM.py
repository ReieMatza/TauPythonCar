from ctypes import *
from Car import *
import csv
import sys
import time
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import threading


# def plotAnimate(i , carStatueQueue ,plotFile ,fieldnames,car):
#     data = pd.read_csv('data.csv')
#     carStatueQueue.queue.clear()
#     x = data['Easting (m)']
#     y = data['Northing (m)']
#     plt.cla()
#     plt.plot(x, y, label='Location')
#     plt.xlim((-2,2))
#     plt.ylim((-2,2))
#     plt.legend(loc='upper left')
#     plt.tight_layout()

# def plotter(carStatueQueue ,plotFile ,fieldnames,car):
#     plt.style.use('fivethirtyeight')
#     ani = FuncAnimation(plt.gcf(), plotAnimate,fargs=(carStatueQueue ,plotFile ,fieldnames,car,), interval=10)
#     plt.tight_layout()
#     plt.show()

def RunSLAM(car,carStatueQueue,trackMap, oppMode):
    firstPacketLocation = True
    firstPacketHeading = True

    trackMap.openMap(carStatueQueue,car)

    if oppMode.type == "online":
        while 1:
                stat = carStatueQueue.get() 
                if stat.type == 1:
                    if firstPacketLocation:
                        car.setZero(stat.location)
                        firstPacketLocation=False
                if stat.type == 2:
                    if firstPacketLocation:
                        car.setZero(stat.location)
                        firstPacketLocation=False
                car.updateStatus(stat,trackMap)

    # elif oppMode.type == "offline":
    #     data = pd.read_csv(oppMode.path)
    #     heading = data['Heading (degrees)']
    #     x = data['Easting (m)']
    #     y = data['Northing (m)']
    #     UNIXseconds = data['Unix Time']
    #     microSeconds = data['Microseconds']
    #     car.setZero([x[0],y[0]])
    #     for i in range(len(x)):
    #         with open(plotFile, 'a') as csv_file:
    #             csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #             info = {"Northing (m)": y[i]-y[0],"Easting (m)": x[i]-x[0] , "Heading (degrees)":((360 +(heading[i]-heading[0]))%360),
    #             "Microseconds":microSeconds[i],"Unix Time":UNIXseconds[i]}
    #             csv_writer.writerow(info)

    #             #to-do add offline updateStatus mode
    #         time.sleep(0.1)
            

    