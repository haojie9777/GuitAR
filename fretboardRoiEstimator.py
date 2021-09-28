import cv2
import numpy


class FretboardRoiEstimator():
    
    def roiSelector(self, frame):
        r = cv2.selectROI(frame)
        
        # Crop image
        roi = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        
        return roi
        
        
    def detectORBKeypoints(self, frame):
        
        # Initiate ORB detector
        orb = cv2.ORB_create()
        
        # find the keypoints with ORB
        kp = orb.detect(frame,None)
        
        # compute the descriptors with ORB
        kp, des = orb.compute(frame, kp)

        # draw only keypoints location,not size and orientation
        img = cv2.drawKeypoints(frame, kp, None, color=(0,255,0), flags=0)
        
        
        return img

    