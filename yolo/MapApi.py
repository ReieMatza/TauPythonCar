import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
import csv
import threading


mapFile = 'data.csv'
fieldnames = ["Unix Time","Microseconds", "Northing (m)", "Easting (m)" ,"Heading (degrees)","Yellow Cone X","Yellow Cone Y","Blue Cone X","Blue Cone Y"]

print("importing TrackMap")
class TrackMap:
    def __init__(self):
        with open(mapFile, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

    #gets the cone X,Y location as ints and the color as string blue/yellow
    def addCone(self,coneX,coneY,color):
        #print('After: ' + str(color) + ' ' + str(coneX) +' ' + str(coneY))
        with open(mapFile, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if color.lower() == 'blue':
                info = {"Blue Cone X": coneX,"Blue Cone Y": coneY}
                csv_writer.writerow(info)
            elif color.lower() == 'yellow':
                info = {"Yellow Cone X": coneX,"Yellow Cone Y": coneY}
                csv_writer.writerow(info)
            
    #location is an array with size of 2, location[0] is y, location[1] in x
    def addCarLocation(self, location):
        with open(mapFile, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {"Northing (m)": location[0],"Easting (m)": location[1]}
            csv_writer.writerow(info)

    def openMap(self):
        plotThread = threading.Thread(target = plotter, daemon=True)
        plotThread.start()


def plotAnimate(i):
    data = pd.read_csv(mapFile)
    x = data['Easting (m)']
    y = data['Northing (m)']
    plt.cla()
    plt.plot(x, y, label='Location')

    xYellowCones = data['Yellow Cone X']
    yYellowCones = data['Yellow Cone Y']
    plt.plot(xYellowCones, yYellowCones,'o',color ='yellow')

    xBlueCones = data['Blue Cone X']
    yBlueCones = data['Blue Cone Y']
    plt.plot(xBlueCones, yBlueCones,'o',color ='blue')


    plt.xlim((-10,10))
    plt.ylim((0,40))
    plt.legend(loc='upper left')
    plt.tight_layout()

def plotter():
    plt.style.use('fivethirtyeight')
    ani = FuncAnimation(plt.gcf(), plotAnimate, interval=10)
    plt.tight_layout()
    plt.show()