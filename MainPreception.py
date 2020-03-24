import sys
import os
dir = os.path.dirname(__file__)
IMUpath = os.path.join(dir, 'IMU')
sys.path.append(IMUpath)
import IMUPython

def main():
    IMUPython.ImuLoop()

if __name__ == "__main__":
    main()