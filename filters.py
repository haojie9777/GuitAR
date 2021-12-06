import cv2
import numpy
import math


def applyGaussianBlur(frame):
    result = cv2.GaussianBlur(frame,(1,3),1)
    return result
    
def getCannyEdge(frame):
    grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    #threshold1, threshold 2. Higher -> less detection
    #recommended threshold ratio 1:2, 1:3
    
    edges = cv2.Canny(grayFrame,100,200,3) #with monitor light on
    return edges

def drawContours(edges,frame):
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    cv2.drawContours(frame,contours, -1, (0,255,0),2)

def applyHoughLines(edges,frame):
    lines = cv2.HoughLinesP(edges,1, numpy.pi/180,50,None,50,10)
    # Draw the lines

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(frame, pt1, pt2, (0,255,0), 1, cv2.LINE_AA)
    return frame

def applyHoughLinesP(edges,frame):
    lines = cv2.HoughLinesP(edges,1, numpy.pi/180,50,None,50,10)
    # Draw the lines
    
    #lines is array consisting of lines w 4 values(start,start,end,end)

    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            cv2.line(frame, (l[0], l[1]), (l[2],l[3]), (0,255,0), 1, cv2.LINE_AA)
    return frame

def applyDilation(frame):
    #kernel = numpy.ones((3,3),numpy.uint8)
    kernel = numpy.ones((2,2),numpy.uint8)
    
    return cv2.dilate(frame,kernel, iterations=1)

def applySobelX(frame):
    sobelx = cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=5)
    return sobelx

def applySobelY(frame):
    sobely = cv2.Sobel(frame,cv2.CV_64F,0,1,ksize=5)
    return sobely

def applyBilateralFilter(frame):
    return cv2.bilateralFilter(frame, 9, 75, 75)
    

def drawPoly(frame, pts: numpy.array):
    isClosed = True
    color = (0,255,0)
    thickness = 2
    
    return cv2.polylines(frame, [pts], isClosed, color, thickness)
    
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


    
    
    

    
    




 
 
    
    

