import cv2
import numpy as np

class SkinDetector():
    
    def __init__(self):
        # define the upper and lower boundaries of the HSV pixel
        # intensities to be considered 'skin'
        self.lower = np.array([0, 58, 30], dtype = "uint8")
        self.upper = np.array([33, 255, 255], dtype = "uint8")
      
    
    def isSkinDetected(self, frame):
        #crop out head of guitar neck, as it results in false positive
        frame = frame[:,:550]
        
        converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        skinMask = cv2.inRange(converted, self.lower, self.upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        skinMask = cv2.erode(skinMask, kernel, iterations = 2)
        skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
        skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)

        #skinHSV = cv2.bitwise_and(frame, frame, mask = skinMask)
        #sufficient pixels similar to skin
        return np.count_nonzero(skinMask) > 8000
      

        
    