import cv2 as cv
import numpy as np
import math
import sys




smileImg = cv.imread("resources/smile.png")
if smileImg.shape == None:
    sys.exit("Smile.png not loaded")

    
    
capture = cv.VideoCapture(0,cv.CAP_DSHOW)

# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")


#dummy function
empty = lambda _: True

#declare GUI for adjusting parameters
cv.namedWindow("Canny Parameters")
cv.resizeWindow("Parameters",640,240)
cv.createTrackbar("Threshold 1", "Canny Parameters",23,255,empty)
cv.createTrackbar("Threshold 2", "Canny Parameters",83,255,empty)

def circularityMeasure(area, perimeter):
    if (perimeter == 0) or (area == 0):
        return False
    circularityValue = (4*math.pi*area)/(perimeter*perimeter)
    #print(circularityValue)
    if circularityValue >= 0.8:
        return True
    else:
        return False
    
def predictShape(numVertices, width, height, area, perimeter):
    aspectRatio = width / float(height)
    if numVertices == 4:
        if aspectRatio >= 0.95:
            return "Rectangle"
        else: 
            return "Square"
    elif numVertices == 3:
        return "Triangle"
    elif numVertices >= 7 and circularityMeasure(area,perimeter):
         return "Circle"
    else:
        return "Others"

def getContours(img,imgContour):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
  
    for c in contours:
        area = cv.contourArea(c)
        
        #only draw significant contours
        if area > 10000:
            cv.drawContours(imgContour,c,-1,(255,0,255),5)
            perimeter = cv.arcLength(c,True)
        
            
            #approx number of points in the contour
            vertices = cv.approxPolyDP(c,0.02*perimeter,True)
            x,y,w,h = cv.boundingRect(vertices)
            
            #circle overlay test
            #if predictShape(len(vertices),w,h,area,perimeter) == "Circle":
            #    smileImg2 = cv.resize(smileImg,(w,h))
            #    imgContour[y:y+h, x:x+w] = smileImg2
            
            cv.rectangle(imgContour, (x,y), (x+w, y+h),(0,255,0),5)
            #display stats about contour
            cv.putText(imgContour, "Vertices: " + str(len(vertices)), (x + w + 20, y + 20),\
                cv.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            cv.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45),\
                cv.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            cv.putText(imgContour, "Shape: " + predictShape(len(vertices),w,h,area,perimeter), (x + w + 20, y + 70),\
                cv.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            cv.putText(imgContour, str(("(x,y): ",x,y)), (x + w + 20, y + 85),\
                cv.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            
while True:
    ret, frame = capture.read() #webcam frame shape: 480 x 640 x 3
    img = frame.copy()
    imgContour = frame.copy()
    print(img.shape)
    
    #apply gaussian blur and convert to grayscale
    imgBlur = cv.GaussianBlur(img,(7,7),1)
    imgGray = cv.cvtColor(imgBlur,cv.COLOR_BGR2GRAY)
    
    #apply
    
    
    #apply canny edge
    #threshold1 = cv.getTrackbarPos("Threshold 1","Canny Paramaters")
    #threshold2 = cv.getTrackbarPos("Threshold 2","Canny Parameters")
    v = np.median(imgGray)
    sigma = 0.33
    threshold1 = int(max(0,(1.0-sigma)*v))
    threshold2 = int(min(255,(1.0+sigma)*v))
    imgCanny = cv.Canny(imgGray, threshold1, threshold2)
    
    #dilation to reduce noise
    kernel = np.ones((10,10))
    imgDil = cv.dilate(imgCanny, kernel, iterations=1)
    
    #apply contours
    getContours(imgDil, imgContour)
    
    combinedImage = cv.hconcat([img,imgContour])
    #cv.imshow("Smiley",smileyFace)
    cv.imshow('Before and After',combinedImage)
    
    if cv.waitKey(20) & 0xFF==ord("d"):
        break


#cleanup
capture.release()
cv.destroyAllWindows()

    
