import cv2
import numpy

def applyGaussianBlur(frame):
    result = cv2.GaussianBlur(frame,(5,5),0)
    return result
    
def getCannyEdge(frame):
    grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    #threshold1, threshold 2. Higher -> less detection
    #recommended threshold ratio 1:2, 1:3
    
    edges = cv2.Canny(grayFrame,100,300,3) #with monitor light on
    return edges

#play around with monitor light to ensure most of the lines are detected
def autoCannyEdge(image, sigma=0.33):
        grayFrame = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    	# compute the median of the single channel pixel intensities
        v = numpy.median(image)
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(grayFrame, lower, upper)
        # return the edged image
        return edged

def drawContours(edges,frame):
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    cv2.drawContours(frame,contours, -1, (0,255,0),2)
    return frame

def applyDilation(frame):
    kernel = numpy.ones((3,3),numpy.uint8)
    return cv2.dilate(frame,kernel, iterations=2)

def applyErosion(frame):
    kernel = numpy.ones((3,3),numpy.uint8)
    return cv2.erode(frame, kernel, iterations=1)

def applyOpening(frame):
    kernel = numpy.ones((1,1),numpy.uint8)
    return cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)


def applyClosing(frame):
    kernel = numpy.ones((7,7),numpy.uint8)
    return cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

def applySobelX(frame): #vertical edges accented
    #sobelx = cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=5)
    sobelx = cv2.Sobel(frame,cv2.CV_8UC1,1,0,ksize=5)
    return sobelx

def applySobelY(frame): #horizontal edges accented
    sobely = cv2.Sobel(frame,cv2.CV_64F,0,1,ksize=5)
    return sobely

def applyBilateralFilter(frame):
    return cv2.bilateralFilter(frame, 5, 75, 75)
    
def applyMedianBlur(frame):
    return cv2.medianBlur(frame, 5)

def drawPoly(frame, pts: numpy.array):
    isClosed = True
    color = (0,255,0)
    thickness = 2
    
    return cv2.polylines(frame, [pts], isClosed, color, thickness)

def applyThreshold(frame, type = "adaptive",lineType = "string"):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray,5)
    
    if type  == "adaptive" and lineType == "string":
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,19,-2)
    elif type  == "adaptive" and lineType == "fret":
         thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,15,-10)
    else:
        thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]
        
    return thresh

    
def applyHoughCircles(frame):
    img = cv2.medianBlur(frame,5)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=50)
    if circles is None:
        return img
    circles = numpy.uint16(numpy.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
    return img



    
    
    

    
    




 
 
    
    

