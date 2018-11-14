#!/usr/bin/env python3

# ---- Imports ----
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt

# ---- Local imports ----
import binarization
import perspective_utils
import hough_lines

# ---- Default values ----
# Webcam path
webcam_path = '/dev/video1'
# Yellow lines threshold
yellow_min = np.array([0, 70, 70])
yellow_max = np.array([50, 255, 255])
kernel = 5


def main():
    video_capture = cv2.VideoCapture(webcam_path)
    while(True):
        ret, frame = video_capture.read()
#        hl_yellow = binarization.highlight_yellow_lines(frame, yellow_min, yellow_max)
#        hl_white = binarization.highlight_white_lines(frame)
#        sobel_edge = binarization.edge_detection(frame, kernel)
#        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#        cv2.imshow('frame-yellow',hl_yellow)
                                      # B G  R
        hough_lines.hough_lines(frame, (0,255,0), 'white')
        hough_lines.hough_lines(frame, (255,0,0), 'yellow')
#        cv2.imshow('frame-white',hl_white)
#        cv2.imshow('frame-sobel',sobel_edge)
        cv2.imshow('frame-gray',frame)
#        cv2.imshow('frame-gray',hl_yellow)
#        birdeye = perspective_utils.birdeye(frame)
#        cv2.imshow('frame-birdeye',birdeye)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
