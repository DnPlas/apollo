import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



#from calibration_utils import calibrate_camera, undistort
#from binarization_utils import binarize
def get_val(y,poly_coeff):
    return poly_coeff[0]*y**2+poly_coeff[1]*y+poly_coeff[2]

def birdeye(image):
    edges=cv2.Canny(image, 50, 150, apertureSize = 3)
    
    h, w = image.shape[:2]
   
    src = np.float32([[(w-10), (h-85)],    # BLUE w, h-191
                      [0,(h-95)],    # GREEN 
                      [70, (h-180)],   # RED
                      [405, (h-180)]])  # CYAN
    dst = np.float32([[w, h],       # br
                      [0, h],       # bl
                      [0, 0],       # tl
                      [w, 0]])      # tr
 
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)
    warped = cv2.warpPerspective(edges, M, (w, h), flags=cv2.INTER_LINEAR)

   
    histogram = np.sum(warped[int(warped.shape[0]/2):,:], axis=0)
        
        # Create an output image to draw on and  visualize the result
    out_img = np.dstack((warped, warped, warped))*255
        
        # we need max for each half of the histogram. the example above shows how
        # things could be complicated if didn't split the image in half
        # before taking the top 2 maxes
    midpoint = np.int(histogram.shape[0]/2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint
    nonzero = warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    leftx_current = leftx_base
    rightx_current = rightx_base
    nwindows = 9
    left_lane_inds = []
    right_lane_inds = []
    # Set the width of the windows +/- margin
    margin = 100
    # Set minimum number of pixels found to recenter window
    minpix = 50
    window_height = np.int(warped.shape[0]/nwindows)
    
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = int(warped.shape[0] - (window+1)*window_height)
        win_y_high = int(warped.shape[0] - window*window_height)
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        # Draw the windows on the visualization image
        cv2.rectangle(out_img,(win_xleft_low,win_y_low),(win_xleft_high,win_y_high),(0,255,0), 3)
        cv2.rectangle(out_img,(win_xright_low,win_y_low),(win_xright_high,win_y_high),(0,255,0), 3)
    
        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]
            # Append these indices to the lists
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
            # If you found > minpix pixels, recenter next window on their mean position
        if len(good_left_inds) > minpix:
            leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:
            rightx_current = np.int(np.mean(nonzerox[good_right_inds]))
    # Concatenate the arrays of indices
    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)
    
    # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]
        
        # Fit a second order polynomial to each
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)
        
        # Generate x and y values for plotting
    ploty = np.linspace(0, warped.shape[0]-1, warped.shape[0] )
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
        
    nonzero = warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    margin = 100
    left_lane_inds = ((nonzerox > (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy + left_fit[2] - margin)) & (nonzerox < (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy + left_fit[2] + margin)))
    right_lane_inds = ((nonzerox > (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy + right_fit[2] - margin)) & (nonzerox < (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy + right_fit[2] + margin)))
        
        # Again, extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]
        # Fit a second order polynomial to each
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)
    
    xm_per_pix = 3.7/700
    image_center = image.shape[1]/2
        
        ## find where lines hit the bottom of the image, closest to the car
    left_low = get_val(image.shape[0],left_fit)
    right_low = get_val(image.shape[0],right_fit)
        
        # pixel coordinate for center of lane
    lane_center = (left_low+right_low)/2.0
        
        ## vehicle offset
    distance = image_center - lane_center
    #points=[left_low, right_low]
    #f, axarray = plt.subplots(1, 2)
    #f.set_facecolor('white')
    #axarray[0].set_title('Before perspective transform')
    #axarray[0].imshow(out_img, cmap='gray')
    ##for point in src:
    #axarray[0].plot(left_low, '.')
    #axarray[0].plot(right_low, '.')
    #
    #axarray[1].set_title('After perspective transform')
    #axarray[1].imshow(warped, cmap='gray')
    #    #for point in dst:
    ##   axarray[1].plot(*point, '.')
    #for axis in axarray:
    #        axis.set_axis_off()
    #
    ##cv2.imshow('linea', warped)
    #plt.show()
    #print('distancia',distance)
    
    theta = np.arctan(float(distance)/6)
    alpha = 90 - theta
    print(theta)
    return warped, out_img
