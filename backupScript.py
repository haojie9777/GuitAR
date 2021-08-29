import cv2 as cv
import numpy as np
from time import time

capture = cv.VideoCapture(0,cv.CAP_DSHOW)


# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")

start = time()
for i in range(120):
    ret, frame = capture.read()
    #to allow video feed to mirror user's setup
    frame = cv.flip(frame,1)
    cv.imshow('Input', frame)
    
    if cv.waitKey(20) & 0xFF==ord("d"):
        break
end = time()
print("FPS: {}".format(120/(end-start)))

#cleanup
capture.release()
cv.destroyAllWindows()

    
