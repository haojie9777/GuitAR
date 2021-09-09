import cv2
import numpy
import math


def applyGaussianBlur(frame):
    result = cv2.GaussianBlur(frame,(1,3),1)
    return result
    
def getCannyEdge(frame):
    grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grayFrame,50,200,3)
    return edges

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

    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            cv2.line(frame, (l[0], l[1]), (l[2],l[3]), (0,255,0), 1, cv2.LINE_AA)
    return frame
    
    




 
 
    
    

