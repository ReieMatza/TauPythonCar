import sys
import pyzed.sl as sl
from signal import signal, SIGINT
import time
import cv2

cam = sl.Camera()

def handler(signal_received, frame):
    cam.disable_recording()
    cam.close()
    sys.exit(0)

signal(SIGINT, handler)

def start():
    path_output = "recoding.svo"
    mat = sl.Mat()
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD1080
    #init.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Z_UP
    #init.depth_mode = sl.DEPTH_MODE.QUALITY
    init.camera_fps = 30

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    err = status
    #recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.LOSSLESS)
    #err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    runtime = sl.RuntimeParameters()
    print("SVO is Recording, use Ctrl-C to stop.")
    frames_recorded = 0

    while True:
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS :
            
            frames_recorded += 1
            cam.retrieve_image(mat, sl.VIEW.LEFT)
            image = mat.get_data()
            print("Frame count: " + str(frames_recorded), end="\r")
            if frames_recorded % 20 == 0:
                cv2.imshow("ZED", image)

start()