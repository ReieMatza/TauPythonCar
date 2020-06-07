import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
import threading


conesList = []

print("Starting TrackMap...")
class TrackMap:
    def __init__(self):
        global conesList
        conesList = []

    #gets the cone X,Y location as ints and the color as string blue/yellow
    def addCones(self,kmeansConesList):
        global conesList
        conesList.clear()
        conesList = kmeansConesList.copy()
        kmeansConesList.clear()

    def openMap(self):
        plotThread = threading.Thread(target = plotter, daemon=True)
        plotThread.start()


def plotAnimate(i):
    global conesList
    plt.clf()
    for cone in conesList:
        print(str(cone[0]) + " " + str(cone[1]) + " -" + cone[2].lower()+ "-")
        plt.plot(cone[0], cone[1],'o',color =cone[2].lower())


    plt.xlim((-10,10))
    plt.ylim((0,40))
    #plt.legend(loc='upper left')
    plt.tight_layout()

def plotter():
    plt.style.use('fivethirtyeight')
    ani = FuncAnimation(plt.gcf(), plotAnimate, interval=10)
    plt.tight_layout()
    plt.show()