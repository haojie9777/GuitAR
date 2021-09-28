import cv2 as cv
import numpy as np
from time import time
import fretboardRoiEstimator

#for fast testing of functionalities

capture = cv.VideoCapture(0,cv.CAP_DSHOW)

fretboardRoiEstimator = fretboardRoiEstimator.FretboardRoiEstimator()

roiSelected = False
savedFrame = np.array(0)

# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = capture.read()
    #to allow video feed to mirror user's setup
    frame = cv.flip(frame,1)
    cv.imshow('Input', frame)
    savedFrame = frame
    if cv.waitKey(20) & 0xFF==ord("d"):
        break

roi = fretboardRoiEstimator.roiSelector(savedFrame)
cv.imshow('ROI',roi)
cv.waitKey(0)

keypoints = fretboardRoiEstimator.detectORBKeypoints(roi)
cv.imshow("ORB keypoints",keypoints)
cv.waitKey(0)    


#cleanup
capture.release()
cv.destroyAllWindows()

    
