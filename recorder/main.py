import threading
import zedRecorder
import queue
from IMUPython import *


statusQueue = queue.Queue() # Global detections queue # , args=(statusQueue,)
carStatueUpdateQueue = queue.Queue()
imuThread = threading.Thread(target = ImuLoop, args =(carStatueUpdateQueue,'data.csv',), daemon=True)

imuThread.start()
car = Car()

recordingThread = threading.Thread(target=zedRecorder.start)
recordingThread.start()


firstPacketLocation = True
firstPacketHeading = True


while 1:
    stat = carStatueUpdateQueue.get() 
    if stat.type == 1:
        if firstPacketLocation:
            car.setZero(stat.location)
            firstPacketLocation=False
    if stat.type == 2:
        if firstPacketHeading:
            car.setZeroHeading(stat.heading)
            firstPacketHeading=False
    car.updateStatusRecorder(stat,statusQueue)



