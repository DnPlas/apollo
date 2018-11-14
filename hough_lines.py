import cv2
import numpy as np
import binarization

yellow_min = np.array([0, 70, 70])
yellow_max = np.array([50, 255, 255])

def hough_lines(img, line_colour,lane_colour):
    if lane_colour is 'yellow':
        hl_frame= binarization.highlight_yellow_lines(img, yellow_min, yellow_max) 
    else:
        hl_frame = binarization.highlight_white_lines(img) 
    edges = cv2.Canny(hl_frame,50, 150, apertureSize = 3)
    lines = cv2.HoughLines(edges,1,np.pi/180,10)

    if lines is not None:
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
       
            cv2.line(img,(x1,y1),(x2,y2),line_colour,2)
