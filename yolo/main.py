import threading
import darknet
import middleMan
import queue
from MapApi import *

detectionsQueue = queue.Queue() # Global detections queue
trackMap = TrackMap()
yolov3Thread = threading.Thread(target=darknet.yolov3, args=(detectionsQueue,))
yolov3Thread.start()
yolov3Thread = threading.Thread(target=middleMan.detectionsQueueLoop, args=(detectionsQueue,trackMap))
yolov3Thread.start()
trackMap.openMap()


