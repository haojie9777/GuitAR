#first get 4 corners of guitar neck 
#Then find sift keypoints of each of them
#in every frame, match each of them with the frame
#obtain centroid of match to get 4 corners of guitar neck
#use drawpoly to obtain guitar neck


import cv2
import time
import numpy
import fretboardRoiEstimator
fretboardRoiEstimator = fretboardRoiEstimator.FretboardRoiEstimator()


#4 corners of fretboard
corners = []
corners_captured = None
save_corners_to_folder = True
load_corners = True

#keypoints
kp = []
#descriptors
des = []

#sift
sift = cv2.SIFT_create()


if load_corners:
    for i in range(1,5):
        img = cv2.imread("corners/corner "+str(i) +".png")
        k,d = fretboardRoiEstimator.detectSIFTKeypoints(img)
        kp.append(k)
        des.append(d)
        
    print("corners preloaded and keypoints computed")
    corners_captured = True
    
 
        
capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)

def roiSelector(frame, corner):
        r = cv2.selectROI(frame)
        # Crop image
        roi = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        corners.append(roi)
        if save_corners_to_folder:
            cv2.imwrite("corners/corner "+str(corner)+".png",roi)
        return roi
    
# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = capture.read()
    frame = cv2.flip(frame,1) 
    
    #capture corners 
    if not corners_captured:
        for i in range(1,5):
            roiSelector(frame,i)
    
    else:
        #get kp of frame
        frameKp,frameDes = fretboardRoiEstimator.detectSIFTKeypoints(frame)
        
        corner_matches = []
        #compute matches
        for i in range(4):
            corner_matches.append(fretboardRoiEstimator.getKeyPointMatchesGeneric(des[i],frameDes))
        
    

        for i in range(4):
              # Get the matching keypoints for each of the images
            for mat in corner_matches[i]:
                img2_idx = mat.trainIdx
            
                # Get the coordinates
                x,y = frameKp[img2_idx].pt
                x = int(x)
                y= int(y)
                
                if x and y:
                    frame = cv2.circle(frame, (x,y), 20, (0,255,0), 2)

     
    #display result
    cv2.imshow('Input', frame)
    
    if cv2.waitKey(10)&0xFF == 27: 
        savedFrame = frame
        break  # esc to quit
    
 
            

