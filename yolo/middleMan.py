import queue
from classes import Detection


def detectionsQueueLoop(detectionsQueue):
    while (True):
        if detectionsQueue.empty() == False:
            detection = detectionsQueue.get()
            print("coneColor: " + detection.coneColor +" camDistance: " + str(detection.camDistance) + " depthDistance: " + str(detection.depthDistance) + " relHeading: " + str(detection.relHeading))


