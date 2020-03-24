import sys
import os
import queue
import threading


dir = os.path.dirname(__file__)
IMUpath = os.path.join(dir, 'IMU')
CARpath = os.path.join(dir, 'Car')
sys.path.append(IMUpath)
sys.path.append(CARpath)
from IMUPython import *

def main():

    imuQ = queue.Queue()
    imuThread = threading.Thread(target = ImuLoop, args =(imuQ,), daemon=True)
    imuThread.start()

    while 1:
        stat = imuQ.get() 
        print(stat.heading)
        

if __name__ == "__main__":
    main()