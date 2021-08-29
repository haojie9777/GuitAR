import cv2
import numpy


def applyGaussianBlur(frame):
    result = cv2.GaussianBlur(frame,(7,7),1)
    return result
    

    
def applyCannyEdge(frame):
    blur = applyGaussianBlur(frame)
    result = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
    return result
 
 
    
    

