import cv2
import numpy as np


class FretboardRoiEstimator():
    
    hasFretboardKeyPoints = False
    fretboardKeyPoints = np.array(0)
    fretboardKeyPointsDes = None
    fretboardKeyPointsImage = np.array(0)

    
   
    
    def roiSelector(self, frame):
        r = cv2.selectROI(frame)
        
        # Crop image
        roi = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        
        return roi
        
     #calibrate true only for inital roi detection of fretboard  
    def detectORBKeypoints(self, frame, calibrate = False):
        
        # Initiate ORB detector
        orb = cv2.ORB_create()
        
        # find the keypoints and descriptors with ORB
        kp, des = orb.detectAndCompute(frame,None)
        
        if calibrate:
            self.fretboardKeyPoints = kp
            self.hasFretboardKeyPoints = True

            # draw only keypoints location,not size and orientation
            self.fretboardKeyPointsImage = cv2.drawKeypoints(frame, kp, None, color=(0,255,0), flags=0)
        else:
            return kp, des
    
    
    
    #calibrate true only for inital roi detection of fretboard
    def detectSIFTKeypoints(self, frame, calibrate = False):
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        #initialize SIFT object
        sift = cv2.SIFT_create()
        
        #get keypoints and descriptors
        kp,des = sift.detectAndCompute(gray,None)
        
        if calibrate:
            self.fretboardKeyPoints = kp
            self.hasFretboardKeyPoints = True
            #self.fretboardKeyPointsImage = cv2.drawKeypoints(frame,kp, None, color=(0,255,0),flags=0)
            self.fretboardKeyPointsImage = frame
            self.fretboardKeyPointsDes = des
        #return keypoints and descriptors
        else:
            return kp, des
         
    
    #return keypoints of fretboard if available
    def getFretboardKeypoints(self):
        if self.hasFretboardKeyPoints:
            return self.fretboardKeyPoints
    
    #return keypoints image of fretboard if available
    def getFretboardKeypointsImage(self):
        if self.hasFretboardKeyPoints:
            return self.fretboardKeyPointsImage
        

    #return matches between frame keypoints des and roi fretboar keypoint des
    def getKeyPointMatches(self, des2):
        
        des1 = self.fretboardKeyPointsDes
        #feature matching
        bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key = lambda x:x.distance)
        return matches
        
        
    