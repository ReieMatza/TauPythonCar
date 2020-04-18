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

def main():

    imuQ = queue.Queue()
    imuThread = threading.Thread(target = ImuLoop, args =(imuQ,), daemon=True)
    imuThread.start()
    car = Car()
    firstPacket = True


    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.show()
    ax.relim() 
    ax.autoscale_view(True,True,True)
    fig.canvas.draw()
    plt.show(block=False)
    pltData = []

    while 1:
        stat = imuQ.get() 
        if stat.heading == 400:
            if firstPacket:
                car.setZero(stat.location)
                firstPacket=False
        
        car.updateStatus(stat)
            
        r = (car.location[0]**2 + car.location[1]**2+car.location[2]**2)**0.5
        # print("x: {0} y: {1} z: {2} r: {3} \n" .format( car.location[0] ,car.location[1], car.location[2],r))
        print("r: {0} \n" .format(r))
        # pltData.append([car.location[0],car.location[1]])
        # ax.plot(pltData,color ="b")
        # fig.canvas.draw()
        # time.sleep(0.5)

            
        

if __name__ == "__main__":
    main()