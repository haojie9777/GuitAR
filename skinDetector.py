import cv2
import numpy as np

class SkinDetector():
    
    def __init__(self):
        pass
    
    # def isSkinDetected(self, frame):
    #     # define the upper and lower boundaries of the HSV pixel
    #     # intensities to be considered 'skin'
    #     lower = np.array([0, 58, 30], dtype = "uint8")
    #     upper = np.array([33, 255, 255], dtype = "uint8")
       
    #     #crop out head of guitar neck, as it results in false positive
    #     frame = frame[:,:550]
        
    #     converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #     skinMask = cv2.inRange(converted, lower, upper)
    #     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    #     #skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    #     #skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    #     #skinMask = cv2.GaussianBlur(skinMask, (5, 5), 0)
    #     cv2.imshow("occlusion", skinMask)

    #     #skinHSV = cv2.bitwise_and(frame, frame, mask = skinMask)
    #     #sufficient pixels similar to skin
    #     return np.count_nonzero(skinMask) > 10000
    
    def isSkinDetected(self, frame):
        min_YCrCb = np.array([0,133,77],np.uint8)
        max_YCrCb = np.array([235,173,127],np.uint8)
       
        #crop out head of guitar neck, as it results in false positive
        frame = frame[:,:550]
        
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
        skinMask = cv2.inRange(converted, min_YCrCb, max_YCrCb)
        skinYCrCb = cv2.bitwise_and(frame, frame, mask = skinMask)
        #sufficient pixels similar to skin
        return np.count_nonzero(skinMask) > 8000
      
      
      
      

        
    