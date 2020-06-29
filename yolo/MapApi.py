import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
import threading
from classes import outputData
import queue

'''
while True:
    if zedFramesQueue.empty() == False:
        frame = zedFramesQueue.get()
        image = frame.image
        camPosition = frame.camOrientation
        camPosition = frame.camPosition

#show the image using cv2.imshow("ZED", image)

'''

conesList = []

print("Starting TrackMap...")
class TrackMap:
    def __init__(self,imageOutputQueue):
        global conesList
        conesList = []
        self.imageOutputQueue = imageOutputQueue

    #gets the cone X,Y location as ints and the color as string blue/yellow
    def addCones(self,kmeansConesList):
        global conesList
        conesList.clear()
        conesList = kmeansConesList.copy()
        kmeansConesList.clear()

    def openMap(self):
        plotThread = threading.Thread(target = plotter, daemon=True,args=(self.imageOutputQueue))
        plotThread.start()


def plotAnimate(i,imageOutputQueue):
    global conesList
    plt.clf()
    img = imageOutputQueue.get()
    fig , axs =  plt.subplots(1,2)
    fig.suptitle('Yolo and cone detections')
    for cone in conesList:
        print(str(cone[0]) + " " + str(cone[1]) + " -" + cone[2].lower()+ "-")
        axs[0].plot(cone[0], cone[1],'o',color =cone[2].lower())
    axs[1].imshow(img)    
    #plt.xlim((-10,30))
    #plt.ylim((0,40))
    #plt.legend(loc='upper left')
    plt.tight_layout()

def plotter(imageOutputQueue):
    plt.style.use('fivethirtyeight')
    ani = FuncAnimation(plt.gcf(), plotAnimate, interval=4,args=(self.imageOutputQueue))
    plt.tight_layout()
    plt.show()