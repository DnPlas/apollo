#!/usr/bin/env python3

# ---- Imports ----
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt

# ---- Local imports ----
import binarization

# ---- Default values ----
# Webcam path
webcam_path = '/dev/video1'
# Yellow lines threshold
yellow_min = np.array([5, 100, 150])
yellow_max = np.array([40, 255, 255])
kernel = 5


def main():
    video_capture = cv2.VideoCapture(webcam_path)
    while(True):
        ret, frame = video_capture.read()
        hl_yellow = binarization.highlight_yellow_lines(frame, yellow_min, yellow_max)
        hl_white = binarization.highlight_white_lines(frame)
        sobel_edge = binarization.edge_detection(frame, kernel)
        cv2.imshow('frame-yellow',hl_yellow)
        #cv2.imshow('frame-white',hl_white)
        #cv2.imshow('frame-sobel',sobel_edge)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
