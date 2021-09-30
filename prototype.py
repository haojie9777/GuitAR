import cv2 as cv
import numpy as np
import fretboardRoiEstimator

#for fast testing of functionalities

capture = cv.VideoCapture(0,cv.CAP_DSHOW)

fretboardRoiEstimator = fretboardRoiEstimator.FretboardRoiEstimator()

roiSelected = False
savedFrame = None
match = None
kp = None

# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = capture.read()
    
    #to allow video feed to mirror user's setup
    frame = cv.flip(frame,1)
    cv.imshow('Input', frame)
    
    keyPoints,des = fretboardRoiEstimator.detectSIFTKeypoints(frame)
    kp = keyPoints
    if fretboardRoiEstimator.hasFretboardKeyPoints:
        matches = fretboardRoiEstimator.getKeyPointMatches(des)
        match = matches
       

    #perform inital roi cropping and getting of keypoints of fretboard
    if cv.waitKey(1) & 0xFF==ord(" ") and fretboardRoiEstimator.hasFretboardKeyPoints == False:
        roi = fretboardRoiEstimator.roiSelector(frame)
        kpImage = fretboardRoiEstimator.detectSIFTKeypoints(roi,calibrate=True)
        
   
    if cv.waitKey(10)&0xFF == 27: 
        savedFrame = frame
        break  # esc to quit
    
# if fretboardRoiEstimator.hasFretboardKeyPoints:
#     # cv.imshow("keypoints",fretboardRoiEstimator.getFretboardKeypointsImage())
#     # cv.waitKey(0)

 
# keyPoints,des = fretboardRoiEstimator.detectSIFTKeypoints(savedFrame)
# kp = keyPoints
# if fretboardRoiEstimator.hasFretboardKeyPoints:
#     matches = fretboardRoiEstimator.getKeyPointMatches(des)
#     match = matches

matchImg = cv.drawMatches(fretboardRoiEstimator.getFretboardKeypointsImage(),fretboardRoiEstimator.getFretboardKeypoints(),savedFrame,kp,match[:50],None, flags=2)
cv.imshow("matches",matchImg)

# cv.imshow("frame",savedFrame)
# cv.imshow("saved guitar neck",fretboardRoiEstimator.getFretboardKeypointsImage())
cv.waitKey(0)
        

#cleanup
capture.release()
cv.destroyAllWindows()

    
