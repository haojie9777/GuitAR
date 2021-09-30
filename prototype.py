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

count = 0
while True:
    ret, frame = capture.read()
    #to allow video feed to mirror user's setup
    frame = cv.flip(frame,1)
    cv.imshow('Input', frame)
   
    #perform keypoint detection of fretboard
    if cv.waitKey(10) & 0xFF==ord(" ") and fretboardRoiEstimator.hasFretboardKeyPoints == False:
        roi = fretboardRoiEstimator.roiSelector(frame)
        kpImage = fretboardRoiEstimator.detectSIFTKeypoints(roi)
        
    #savedFrame = frame
    if cv.waitKey(10) & 0xFF==ord("d"):
        break
    
if fretboardRoiEstimator.hasFretboardKeyPoints:
    cv.imshow("keypoints",fretboardRoiEstimator.getFretboardKeypointsImage())
    cv.waitKey(0)
        

# roi = fretboardRoiEstimator.roiSelector(savedFrame)
# cv.imshow('ROI',roi)
# cv.waitKey(0)

# keypoints = fretboardRoiEstimator.detectSIFTKeypoints(roi)
# cv.imshow("SIFT keypoints",keypoints)
# cv.waitKey(0)    


#cleanup
capture.release()
cv.destroyAllWindows()

    
