import threading
import darknet
import middleMan
import queue

detectionsQueue = queue.Queue() # Global detections queue

yolov3Thread = threading.Thread(target=darknet.yolov3, args=(detectionsQueue,))
yolov3Thread.start()
yolov3Thread = threading.Thread(target=middleMan.detectionsQueueLoop, args=(detectionsQueue,))
yolov3Thread.start()


