from typing import no_type_check_decorator
import cv2
import numpy as np
import math
from collections import defaultdict


def drawVerticalLines(lines, frame):
    if lines is None:
        return
    
            
    
    import cv2
import numpy as np

def removeDuplicateLines(lines):
    if lines is None:
        return
    strong_lines = np.zeros([6,1,2])
        
    n2 = 0
    for n1 in range(0,len(lines)):
        for rho,theta in lines[n1]:
            if n2 == 6: #added this line
                return strong_lines
            if n1 == 0:
                strong_lines[n2] = lines[n1]
                n2 = n2 + 1
            else:
                if rho < 0:
                    rho*=-1
                    theta-=np.pi
                closeness_rho = np.isclose(rho,strong_lines[0:n2,0,0],atol = 10)
                closeness_theta = np.isclose(theta,strong_lines[0:n2,0,1],atol = np.pi/36)
                closeness = np.all([closeness_rho,closeness_theta],axis=0)
                if not any(closeness) and n2 < 6:
                        strong_lines[n2] = lines[n1]
                        n2 = n2 + 1
                        
    #maybe remove line that has a very different theta than the rest 
    return strong_lines


def drawFrets(lines,frame):
    if lines is None:
        return

    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 800*(-b)), int(y0 - 800*(a)))
        cv2.line(frame, pt1, pt2, (0,255,0), 1, cv2.LINE_AA)
        print(theta)
        return frame
    
    
def segment_by_angle_kmeans(lines, k=2, **kwargs):
    """Groups lines based on angle with k-means.

    Uses k-means on the coordinates of the angle on the unit circle 
    to segment `k` angles inside `lines`.
    """

    # Define criteria = (type, max_iter, epsilon)
    default_criteria_type = cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER
    criteria = kwargs.get('criteria', (default_criteria_type, 10, 1.0))
    flags = kwargs.get('flags', cv2.KMEANS_RANDOM_CENTERS)
    attempts = kwargs.get('attempts', 10)
    
    #lines = removeDuplicateLines(lines)

    # returns angles in [0, pi] in radians
    angles = np.array([line[0][1] for line in lines])
    # multiply the angles by two and find coordinates of that angle
    pts = np.array([[np.cos(2*angle), np.sin(2*angle)]
                    for angle in angles], dtype=np.float32)

    # run kmeans on the coords
    labels, centers = cv2.kmeans(pts, k, None, criteria, attempts, flags)[1:]
    labels = labels.reshape(-1)  # transpose to row vec

    # segment lines based on their kmeans label
    segmented = defaultdict(list)
    for i, line in enumerate(lines):
        segmented[labels[i]].append(line)
    segmented = list(segmented.values())
    print(segmented)
    return segmented


def returnSlopeOfLine(line):
    if line is None:
        return
    dx = (line[2]- line[0])
    #return 100 instead of infinity if slope is vertical
    if dx == 0 :
        return 100
    slope = round((line[3] - line[1]) / dx,2)
  
    return slope

def applyHoughLines(edges,frame): 
    #lines = cv2.HoughLines(edges, 1, 2*numpy.pi / 180, 150)
    lines = cv2.HoughLines(edges, 1, 2*np.pi / 180, 150)
    # Draw the lines
    
    #remove lines similar to one another
    lines = removeDuplicateLines(lines)
    
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 800*(-b)), int(y0 - 800*(a)))
            cv2.line(frame, pt1, pt2, (0,255,0), 1, cv2.LINE_AA)
   
def getHoughLines(edges): 
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)
    
    #remove lines similar to one another
    lines = removeDuplicateLines(lines)
    return lines

            
def applyHoughLinesP(edges, frame):
    #lines are 2d arrays consisting of lines w 4 values: Xstart,Ystart,Xend,Yend)
    #lines = cv2.HoughLinesP(edges, rho=1, theta=numpy.pi / 180
    #,threshold=50, minLineLength=30, maxLineGap=5)
    
    lines = cv2.HoughLinesP(edges, rho=1, theta= 2 * np.pi / 180
    ,threshold=30, minLineLength=30, maxLineGap=3)
    #print(houghProcessing.returnAngleOfLine(lines))
    
    # Draw the lines
    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            
            # #attempt to show only short lines
            # distance = math.sqrt( (l[2] - l[0])**2 + (l[3]- l[1])**2)
            # if distance < 200:
            slope = returnSlopeOfLine(l)
            if slope < 100 and slope >= 1:
                cv2.line(frame, (l[0], l[1]), (l[2],l[3]), (0,255,255), 1, cv2.LINE_AA)
    return frame

def getHoughLinesP(edges):
    #lines are 2d arrays consisting of lines w 4 values: Xstart,Ystart,Xend,Yend)
    lines = cv2.HoughLinesP(edges, rho=1, theta= 2 * np.pi / 180
    ,threshold=30, minLineLength=30, maxLineGap=3)
    return lines


        
        
    





        
        
        