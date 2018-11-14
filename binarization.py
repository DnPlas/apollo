import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt

# ---- Default values ----

# Highlight YELLOW lines
def highlight_yellow_lines(frame, min_values, max_values):

    # Converts frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Check whether the threshold was reached or not
    mask = cv2.inRange(hsv, min_values, max_values)
    
    # Only yellow coloured objects are highlighted and stored
#    highlighted_yellows = cv2.bitwise_and(frame, frame, mask=mask)

    return mask #highlighted_yellows

# Highlight WHITE lines
def highlight_white_lines(frame):

    # Converts frame to gray scale and improves the contrast
    # in the frame using cv2.equalizeHist()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    equalize_gray = cv2.equalizeHist(gray)

    # Filter image with threshold
    _, white_th = cv2.threshold(equalize_gray,250, 255, type=cv2.THRESH_BINARY
)

    return white_th

# Sobel edge detection
def edge_detection(frame, kernel):
    
    # Converts frame to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Convolute with kernels
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel)

    sobel_mag = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
    sobel_mag = np.uint8(sobel_mag / np.max(sobel_mag) * 255)

    return sobel_mag

# Highlights lane-lines from a frame
#def highlight_lanes(frame):

#def binarize(img, verbose=False):
#    """
#    Convert an input frame to a binary image which highlight as most as possible the lane-lines.
#    :param img: input color frame
#    :param verbose: if True, show intermediate results
#    :return: binarized frame
#    """
#    h, w = img.shape[:2]
#
#    binary = np.zeros(shape=(h, w), dtype=np.uint8)
#
#    # highlight yellow lines by threshold in HSV color space
#    HSV_yellow_mask = thresh_frame_in_HSV(img, yellow_HSV_th_min, yellow_HSV_th_max, verbose=False)
#    binary = np.logical_or(binary, HSV_yellow_mask)
#
#    # highlight white lines by thresholding the equalized frame
#    eq_white_mask = get_binary_from_equalized_grayscale(img)
#    binary = np.logical_or(binary, eq_white_mask)
#
#    # get Sobel binary mask (thresholded gradients)
#    sobel_mask = thresh_frame_sobel(img, kernel_size=9)
#    binary = np.logical_or(binary, sobel_mask)
#
#    # apply a light morphology to "fill the gaps" in the binary image
#    kernel = np.ones((5, 5), np.uint8)
#    closing = cv2.morphologyEx(binary.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
#
#    if verbose:
#        f, ax = plt.subplots(2, 3)
#        f.set_facecolor('white')
#        ax[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#        ax[0, 0].set_title('input_frame')
#        ax[0, 0].set_axis_off()
#        ax[0, 0].set_axis_bgcolor('red')
#        ax[0, 1].imshow(eq_white_mask, cmap='gray')
#        ax[0, 1].set_title('white mask')
#        ax[0, 1].set_axis_off()
#
#        ax[0, 2].imshow(HSV_yellow_mask, cmap='gray')
#        ax[0, 2].set_title('yellow mask')
#        ax[0, 2].set_axis_off()
#
#        ax[1, 0].imshow(sobel_mask, cmap='gray')
#        ax[1, 0].set_title('sobel mask')
#        ax[1, 0].set_axis_off()
#
#        ax[1, 1].imshow(binary, cmap='gray')
#        ax[1, 1].set_title('before closure')
#        ax[1, 1].set_axis_off()
#
#        ax[1, 2].imshow(closing, cmap='gray')
#        ax[1, 2].set_title('after closure')
#        ax[1, 2].set_axis_off()
#        plt.show()
#
#    return closing
#
#cap = cv2.VideoCapture('/dev/video1')
#while(True):
#    # Capture frame-by-frame
#    ret, frame = cap.read()
##    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#    HSV_yellow_mask = thresh_frame_in_HSV(frame, yellow_HSV_th_min, yellow_HSV_th_max, verbose=False)
#    final_img = HSV_yellow_mask
##    final_img = binarize(frame, verbose=False)
#    plt.imshow(final_img, cmap='gray')
#    plt.show()
#
##    cv2.imshow('frame',gray)
#
##    if cv2.waitKey(1) & 0xFF == ord('q'):
##        break
#
#
#
##
## When everything done, release the capture
#cap.release()
#cv2.destroyAllWindows()
