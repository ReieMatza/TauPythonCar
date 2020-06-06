import threading
import zedRecorder


#statusQueue = queue.Queue() # Global detections queue # , args=(statusQueue,)

recordingThread = threading.Thread(target=zedRecorder.start)
recordingThread.start()


