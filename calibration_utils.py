import cv2
import glob
import os
import numpy as np

def calibrate_camera(n, m, testdir, fmt, dev=False):

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    print('Start calibration')
    objp = np.zeros((m * n, 3), np.float32)
    objp[:, :2] = np.mgrid[0:n, 0:m].T.reshape(-1, 2)
    
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane.
    
    # Make a list of calibration images
    testdir = os.path.join(testdir, '*'+fmt)
    images = glob.glob(testdir)
    # Step through the list and search for chessboard corners
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chessboard corners
        pattern_found, corners = cv2.findChessboardCorners(gray, (n, m), None
    )
        if pattern_found is True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners,(9,9),(-1,-1),criteria)
            imgpoints.append(corners2)
        
            if dev:
                img = cv2.drawChessboardCorners(img, (n, m), corners, pattern_found)
                cv2.imshow('img',img)
                cv2.waitKey(500)
                cv2.destroyAllWindows()
    
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    return ret, mtx, dist, rvecs, tvecs

def undistort(frame, mtx, dist, dev=False):
    h,  w = frame.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    frame_undistorted = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    if dev:
        cv2.imshow('Distorted', frame)
        cv2.imshow('Undistorted', frame_undistorted)
        cv2.waitKey(9000)
        cv2.destroyAllWindows()
    return frame_undistorted

if __name__ == '__main__':
    n,m = 7,7
    fmt = '.png'
    testdir = '/home/dnplas/dplascen-dev/apollo/test_images/camera_calibration/'
    frame = cv2.imread('/home/dnplas/dplascen-dev/apollo/test_images/camera_calibration/opencv_frame_14.png')
    ret, mtx, dist, rvecs, tvecs = calibrate_camera(n,m,testdir,fmt)
    u_img = undistort(frame, mtx, dist)
    cv2.imshow('u-img',u_img)
    cv2.waitKey(5000000)
    cv2.destroyAllWindows()
