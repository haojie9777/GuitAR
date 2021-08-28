import cv2 as cv
import numpy as np

capture = cv.VideoCapture(0,cv.CAP_DSHOW)

# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = capture.read()
    #to allow video feed to mirror user's setup
    frame = cv.flip(frame,1)
    
    cv.imshow('Input', frame)
    
    if cv.waitKey(20) & 0xFF==ord("d"):
        break

#cleanup
capture.release()
cv.destroyAllWindows()

    
