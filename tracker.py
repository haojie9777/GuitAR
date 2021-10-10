import cv2 as cv
import numpy as np
import fretboardRoiEstimator

#for fast testing of functionalities

roiSelected = False

capture = cv.VideoCapture(0,cv.CAP_DSHOW)

#create kcf tracker
global tracker
tracker = cv.legacy.TrackerCSRT_create()
tracker_ready = False


def roiSelector(frame):
        r = cv.selectROI(frame)
        # Crop image
        roi = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        ok = tracker.init(frame, r)
        return roi
    
    
# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")

# Initialize tracker with first frame and bounding box

while True:
    ret, frame = capture.read()

    #to allow video feed to mirror user's setup
    frame = cv.flip(frame,1)  
    if not roiSelected:
        roiSelector(frame)
        roiSelected = True
        tracker_ready = True
    if tracker_ready:
        ok, bbox = tracker.update(frame)
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else:
            cv.putText(frame, "Tracking failure detected", (100,80), 
            cv.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            

            
        
    
    #display result
    cv.imshow('Input', frame)
    
    if cv.waitKey(10)&0xFF == 27: 
        savedFrame = frame
        break  # esc to quit
    



#cleanup
capture.release()
cv.destroyAllWindows()

    
