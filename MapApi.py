import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
import csv
import threading

mapFile = 'data.csv'
fieldnames = ["Unix Time","Microseconds", "Northing (m)", "Easting (m)" ,"Heading (degrees)"]

print("importing TrackMap")
class TrackMap:
    def __init__(self):
        with open(mapFile, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

    def addCarLocation(self, location):
        with open(mapFile, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {"Northing (m)": location[0],"Easting (m)": location[1]}
            csv_writer.writerow(info)

    def openMap(self,carStatueQueue,car):
        plotThread = threading.Thread(target = plotter, args =(carStatueQueue ,car,), daemon=True)
        plotThread.start()


def plotAnimate(i , carStatueQueue ,car):
    data = pd.read_csv(mapFile)
    carStatueQueue.queue.clear()
    x = data['Easting (m)']
    y = data['Northing (m)']
    plt.cla()
    plt.plot(x, y, label='Location')
    plt.xlim((-2,2))
    plt.ylim((-2,2))
    plt.legend(loc='upper left')
    plt.tight_layout()

def plotter(carStatueQueue ,car):
    plt.style.use('fivethirtyeight')
    ani = FuncAnimation(plt.gcf(), plotAnimate,fargs=(carStatueQueue ,car,), interval=10)
    plt.tight_layout()
    plt.show()