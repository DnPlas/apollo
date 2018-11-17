#!/usr/bin/env python3

# ---- Imports ----
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
import time
# ---- Local imports ----
import binarization
import perspective_utils
import hough_lines
import vehicle_offset
import calibration_utils

# ---- Default values ----
# Webcam paths
webcam_path = '/dev/video1'

# Calibration utils
testdir = '/home/dnplas/dplascen-dev/apollo/test_images/camera_calibration/'
fmt='.png'
n,m = 7,7
# Yellow lines threshold
yellow_min = np.array([0, 70, 70])
yellow_max = np.array([50, 255, 255])
kernel = 5

def main():
    video_capture = cv2.VideoCapture(webcam_path)
    time.sleep(10)
    ret, mtx, dist, rvecs, tvecs = calibration_utils.calibrate_camera(n,m,testdir,fmt)
    while(True):
        ret, frame = video_capture.read()
        time.sleep(10)
#        hl_yellow = binarization.highlight_yellow_lines(frame, yellow_min, yellow_max)
#        hl_white = binarization.highlight_white_lines(frame)
#        sobel_edge = binarization.edge_detection(frame, kernel)
#        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#        vehicle_off = vehicle_offset.vehicle_offset(frame)
#        cv2.imshow('frame-yellow',hl_yellow)
                                      # B G  R
#        hough_lines.hough_lines(frame, (0,255,0), 'white')
#        hough_lines.hough_lines(frame, (255,0,0), 'yellow')
#        cv2.imshow('frame-white',hl_white)
#        cv2.imshow('frame-sobel',sobel_edge)
#        cv2.imshow('frame-gray',gray)
        undist_img = calibration_utils.undistort(frame, mtx, dist)
#        cv2.imshow('frame-undistorted', undist_img)
#        cv2.imshow('frame-gray',hl_yellow)
#        birdeye = perspective_utils.birdeye(frame)
        time.sleep(10)
        perspective_utils.birdeye(undist_img)
        cv2.imshow('frame-birdeye',birdeye)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
