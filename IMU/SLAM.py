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


def plotAnimate(i , carStatueQueue ,plotFile ,fieldnames,car):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y = data['y_value']
    plt.cla()
    plt.plot(x, y, label='Location')
    plt.legend(loc='upper left')
    plt.tight_layout()

def plotter(carStatueQueue ,plotFile ,fieldnames,car):
    plt.style.use('fivethirtyeight')
    ani = FuncAnimation(plt.gcf(), plotAnimate,fargs=(carStatueQueue ,plotFile ,fieldnames,car,), interval=10)
    plt.tight_layout()
    plt.show()

def RunSLAM(car,carStatueQueue,plotFile,fieldnames):
    firstPacket = True
    plotThread = threading.Thread(target = plotter, args =(carStatueQueue ,plotFile ,fieldnames,car,), daemon=True)
    plotThread.start()
    while 1:
            stat = carStatueQueue.get() 
            # carStatueQueue.queue.clear()
            if stat.type == 1:
                if firstPacket:
                    car.setZero(stat.location)
                    firstPacket=False
            
            car.updateStatus(stat,plotFile,fieldnames)
                
            r = (car.location[0]**2 + car.location[1]**2+car.location[2]**2)**0.5
            # print("x: {0} y: {1} z: {2} r: {3} \n" .format( car.location[0] ,car.location[1], car.location[2],r))
            print("r: {0} \n" .format(r))

    