import cv2
import numpy as np

class SkinDetector():
    
    def __init__(self):
        # define the upper and lower boundaries of the HSV pixel
        # intensities to be considered 'skin'
        self.lower = np.array([0, 58, 30], dtype = "uint8")
        self.upper = np.array([33, 255, 255], dtype = "uint8")
      
    
    def isSkinDetected(self, frame):
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        skinMask = cv2.inRange(converted, self.lower, self.upper)
        #sufficient pixels similar to skin
        return np.count_nonzero(skinMask) > 20000
        #skinHSV = cv2.bitwise_and(frame, frame, mask = skinMask)

        
        
