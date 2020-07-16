import threading
import darknet
import middleMan
import queue
import zed
from MapApi import *


zedFramesQueue = queue.Queue(maxsize=1)
detectionsQueue = queue.Queue(maxsize=1) # Global detections queue
imageOutputQueue = queue.Queue(maxsize=1)


trackMap = TrackMap(imageOutputQueue)

zedThread = threading.Thread(target=zed.zedGrabber, args=(zedFramesQueue,))
zedThread.start()
yolov3Thread = threading.Thread(target=darknet.yolov3, args=(zedFramesQueue,detectionsQueue,imageOutputQueue))
yolov3Thread.start()
yolov3Thread = threading.Thread(target=middleMan.detectionsQueueLoop, args=(detectionsQueue,trackMap))
yolov3Thread.start()


#imageOutputQueue should be passed to Map
trackMap.openMap()


