import time
from random import randint
import math
import numpy as np
import cv2
import pyzed.sl as sl
#from sympy import symbols, Eq, solve
import queue
from classes import zedFrame


def rotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated


def zedGrabber(zedFramesQueue):

    svo_path = "HD1080.svo"
    zed_id = 0
    init_mode = 0

    input_type = sl.InputType()
    if init_mode == 0:      
        input_type.set_from_svo_file(svo_path)
    else:
        input_type.set_from_camera_id(zed_id)


    init = sl.InitParameters(input_t=input_type)
    init.camera_resolution = sl.RESOLUTION.HD1080
    init.camera_fps = 30
    init.coordinate_units = sl.UNIT.METER
    init.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Z_UP

    cam = sl.Camera()
    if not cam.is_opened():
        print("Opening ZED Camera...")
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        log.error(repr(status))
        exit()

    # Enable positional tracking with default parameters
    py_transform = sl.Transform()  # First create a Transform object for TrackingParameters object
    tracking_parameters = sl.PositionalTrackingParameters(init_pos=py_transform)
    err = cam.enable_positional_tracking(tracking_parameters)

    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    zed_pose = sl.Pose()
    runtime = sl.RuntimeParameters()

    # Use STANDARD sensing mode
    runtime.sensing_mode = sl.SENSING_MODE.STANDARD
    mat = sl.Mat()
    point_cloud_mat = sl.Mat()

    # Import the global variables. This lets us instance Darknet once,


    while True:

        start_time = time.time() # start time of the loop
        err = cam.grab(runtime)

        if (err != sl.ERROR_CODE.SUCCESS):
            break

        cam.retrieve_image(mat, sl.VIEW.LEFT)
        image = mat.get_data()

        cam.retrieve_measure(point_cloud_mat, sl.MEASURE.XYZRGBA)
        depth = point_cloud_mat.get_data()
        cam.get_position(zed_pose, sl.REFERENCE_FRAME.WORLD)

        py_translation = sl.Translation()
        tx = round(zed_pose.get_translation(py_translation).get()[0], 3)
        ty = round(zed_pose.get_translation(py_translation).get()[1], 3)
        tz = round(zed_pose.get_translation(py_translation).get()[2], 3)
        camPosition = (tx, ty, tz)
            #print("Translation: Tx: {0}, Ty: {1}, Tz {2}, Timestamp: {3}".format(tx, ty, tz, zed_pose.timestamp.get_milliseconds()))
        camOrientation = zed_pose.get_rotation_vector()*180/math.pi
        image = rotate(image, -camOrientation[1], center = None, scale = 1.0)
        FPS = 1.0 / (time.time() - start_time)
            # Do the detection
        #rawDetections = detect(netMain, metaMain, image, thresh)
        #detectionsList = detectionsAnalayzer(rawDetections, depth)
        frame = zedFrame(image, depth, camOrientation, camPosition, FPS)
        zedFramesQueue.put(frame)
        #image = cvDrawBoxes(detectionsList, image)
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #image = cv2.resize(image,(1280,720),interpolation=cv2.INTER_LINEAR)
    cam.close()

