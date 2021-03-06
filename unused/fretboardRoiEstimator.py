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
        # bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
        # matches = bf.match(des1, des2)
        # matches = sorted(matches, key = lambda x:x.distance)
        
    
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1,des2,k=2)
    
        good =[]
      
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)
        return good
        #return matches
        
        
        
    #return matches between frame keypoints des and roi fretboar keypoint des
    def getKeyPointMatchesGeneric(self, des1, des2):
        
        #feature matching
        # bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
        # matches = bf.match(des1, des2)
        # matches = sorted(matches, key = lambda x:x.distance)
        
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1,des2,k=2)
        
    
        good =[]
      
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)
        return good
        #return matches
        
        
    def getHomographyMatrix(self, kp1, kp2, matches):
        
        # Sort them in the order of their distance.
        #matches = sorted(matches, key = lambda x:x.distance)
        #matches = matches[:10]
        
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)
        homographyMatrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        
        mask = mask.ravel().tolist()
        
        return homographyMatrix, mask
    
    def getBoundingBox(self, homographyMatrix):
        h,w = self.getFretboardKeypointsImage().shape[:2]
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,homographyMatrix)
        #dst += (w, 0)  # adding offset
        return dst
        
       
