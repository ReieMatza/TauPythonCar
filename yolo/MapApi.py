import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
import threading
from classes import outputData
import queue
import cv2
import io
import math
import numpy as np


def get_img_from_fig(fig, dpi=100):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    return img

def findColsest(x,y, conelistX,conelistY):
    distances =[]
    for i in range(len(conelistX)):
        distances.append(math.sqrt(math.pow(conelistX[i]-x,2) + math.pow(conelistY[i]-y,2)))
    # print(distances)
    return distances.index(min(distances))

def findCenterLine(sortedBlueConesX,sortedBlueConesY,sortedYellowConesX,sortedYellowConesY):
    centerLineX = []
    centerLineY = []
    if  len(sortedBlueConesX) == 0  or len(sortedYellowConesX) == 0:
        return 0,0

    if len(sortedBlueConesX) >= len(sortedYellowConesX):
        longListX = sortedBlueConesX
        longListY = sortedBlueConesY
        shortListX = sortedYellowConesX
        shortListY = sortedYellowConesY
    else:
        longListX = sortedYellowConesX
        longListY = sortedYellowConesY
        shortListX = sortedBlueConesX
        shortListY = sortedBlueConesY

    for i in range(len(longListX)):
        closest = findColsest(longListX[i],longListY[i],shortListX,shortListY)
        centerLineX.append((longListX[i]+shortListX[closest])/2)
        centerLineY.append((longListY[i]+shortListY[closest])/2)
    
    return centerLineX ,centerLineY



def getMinimumDistance(coneList,x,y):
    distances =[]
    for cone in coneList:
        distances.append(math.sqrt(math.pow(cone[0]-x,2) + math.pow(cone[1]-y,2)))
    return distances.index(min(distances))
    


def sortCones(conelist,i):
    
    sortedList = []

    for i in range(len(conelist)):
        if i == 0:
            closestIndex = getMinimumDistance(conelist,0,0)
            sortedList.append(conelist[closestIndex])
            conelist.remove(conelist[closestIndex])

        else:
            closestIndex = getMinimumDistance(conelist,sortedList[i-1][0],sortedList[i-1][1])
            sortedList.append(conelist[closestIndex])
            conelist.remove(conelist[closestIndex])
    

    return sortedList


class TrackMap:
    def __init__(self,imageOutputQueue):

        self.conesList = []
        self.imageOutputQueue = imageOutputQueue

    #gets the cone X,Y location as ints and the color as string blue/yellow
    def updateConeList(self,kmeansConesList):
        
        self.conesList.clear()
        self.conesList = kmeansConesList.copy()
        kmeansConesList.clear()

    def openMap(self):
        plotThread = threading.Thread(target = self.plotter, daemon=True,args=(self.imageOutputQueue,))
        plotThread.start()


    def plotter(self, imageOutputQueue):
        print("showing images")
        fig = plt.figure()
        closingDistance = 7


        out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 20.0, (1920,1080))

        while(1):
            try:
                img = imageOutputQueue.get(timeout = 2)
                plt.title("Map")

                coneLineXBlue =[]
                coneLineYBlue =[]

                coneLineXYELLOW = []
                coneLineYYELLOW = []
                
                #Creating Map
                plt.cla()

                plt.title("Track Map")

                coneList = sortCones(self.conesList.copy(),0)
                for cone in coneList:
                    plt.plot(cone[0], cone[1],'o',color =cone[2].lower())
                    if cone[2] == 'BLUE':
                        coneLineXBlue.append(cone[0])
                        coneLineYBlue.append(cone[1])
                    else:
                        coneLineXYELLOW.append(cone[0])
                        coneLineYYELLOW.append(cone[1])

                #plotting center line
                centerX, centerY = findCenterLine(coneLineXBlue,coneLineYBlue,coneLineXYELLOW,coneLineYYELLOW)
                plt.plot(centerX,centerY,':',color = "black")
                
                if centerX != 0:
                    # if(math.sqrt(math.pow(centerX[0]-centerX[-1],2) + math.pow(centerY[0]-centerY[-1],2)) < closingDistance):
                    centerX.append(centerX[0])
                    centerY.append(centerY[0])

                if len(coneLineYBlue)>1:
                    # if(math.sqrt(math.pow(coneLineXBlue[0]-coneLineXBlue[-1],2) + math.pow(coneLineYBlue[0]-coneLineYBlue[-1],2)) < closingDistance):
                    coneLineXBlue.append(coneLineXBlue[0])
                    coneLineYBlue.append(coneLineYBlue[0])
                if len(coneLineYYELLOW)>1:
                    # if(math.sqrt(math.pow(coneLineXYELLOW[0]-coneLineXYELLOW[-1],2) + math.pow(coneLineYYELLOW[0]-coneLineYYELLOW[-1],2)) < closingDistance):
                    coneLineYYELLOW.append(coneLineYYELLOW[0])
                    coneLineXYELLOW.append(coneLineXYELLOW[0])
                
                plt.plot(coneLineXBlue,coneLineYBlue, color = "blue")
                plt.plot(coneLineXYELLOW,coneLineYYELLOW, color = "yellow")

                # Plotting the car on the map
                plt.plot(img.camPosition[0],img.camPosition[1],'x', color ="RED",)
                # adding the headring signe
                heading = img.camOrientation[2]
                headingLineX = img.camPosition[0] + -1.5 * math.sin(math.radians(heading))
                headingLineY = img.camPosition[1] + 1.5 * math.cos(math.radians(heading))
                plt.plot([img.camPosition[0],headingLineX],[img.camPosition[1],headingLineY],':',color ="RED")



                plot_img_np = get_img_from_fig(fig)            
                img = img.image
                scale_percent = plot_img_np.shape[1]/img.shape[1]
                width = int(img.shape[1] * scale_percent )
                height  = plot_img_np.shape[0]
                dim = (width, height)

                # resize image
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                vis = np.concatenate((resized, plot_img_np), axis=1)
                out.write(vis)
                cv2.imshow("YOLO IMAGE",vis)
                cv2.waitKey(8)
            except queue.Empty:
                print("video done")
                out.release()
                cv2.destroyAllWindows() 
                break



        

