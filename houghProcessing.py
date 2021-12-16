import cv2
import numpy as np
import math

"""
Handles all line processing related utilities 
"""


def removeDuplicateLines(lines):
    if lines is None:
        return
    strong_lines = np.zeros([7,1,2])
        
    n2 = 0
    for n1 in range(0,len(lines)):
        for rho,theta in lines[n1]:
            if n2 == 7: #added this line
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
                if not any(closeness) and n2 < 7:
                        strong_lines[n2] = lines[n1]
                        n2 = n2 + 1
                        
    #maybe remove line that has a very different theta than the rest 
    return strong_lines


def drawStrings(lines,frame):
    if lines is None:
        return frame

    for i in range(0, len(lines)):
        rho = lines[i][0]
        theta = lines[i][1]
        #remove vertical lines and completed horizontal lines
        if theta >= 1.5:
            break
    
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
     
        pt1 = (int(x0 + 0.5*(-b) ), int(y0 + 0.5*(a)) )
        pt2 = (int(x0 - 700*(-b)), int(y0 - 700*(a)))
        cv2.line(frame, pt1, pt2, (0,255,0), 1, cv2.LINE_AA)
        #print(f"pt1:{pt1} pt2:{pt2}")
    return frame

'''
Return points of line segment from string lines defined in theta and rho
'''
def getStringLinePoints(lines):
    result = []
    if lines is None:
        return
    for i in range(0, len(lines)):
        rho = lines[i][0]
        theta = lines[i][1]
    #remove vertical lines and horizontal lines
        if theta >= 1.5:
            break
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
      
        #initial set of points that are too long
        pt1 = (int(x0 + 0.5*(-b) ), int(y0 + 0.5*(a)))
        pt2 = (int(x0 - 700*(-b)), int(y0 - 700*(a)))
        
        #want to tranpose the line segment to around 5th fret height, thus use line equation to find new set of starting points
        gradient = float( (pt2[1] - pt1[1]) / (pt2[0] - pt1[0]))
        new_x_pt1 = pt1[0] + 80 #shift the new x coordinate by 80 pixels
        new_y_pt1 = gradient*(new_x_pt1) - gradient*pt1[0] + pt1[1]
        
        new_pt1 = (int(new_x_pt1),int(new_y_pt1))
    
        result.append([new_pt1,pt2])
    return result
    
    
    
    
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
    lines = cv2.HoughLines(edges, 1, 1*np.pi / 180, 150)
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
    return frame
   
def getHoughLines(edges): 
    lines = cv2.HoughLines(edges, 1, 1*np.pi / 180, 150)
    
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


def processFretLines(lines):
    if lines is None:
        return
    frets = []
    for i in range(0, len(lines)):
        l = lines[i][0]
        slope = returnSlopeOfLine(l)
        if (slope < 100) and (slope >= 1):
            #remove lines that are not likely to be frets
            frets.append(l)
            
    return frets #list of numpy arrays containing 4 points

def removeVerticalLines(lines):
    result = []
    if lines is None:
        return result
    for i in range(len(lines)):
                if lines[i][0][1] <= 2:
                    result.append(lines[i][0])
    return result

            
    
'''
Remove unwanted lines detected, by using 2-means clustering
lines belonging in the largest cluster are assumed to be detected strings,
and will be returned
'''
def processStringLinesByKmeans(lines):
    if lines is None:
        return
    

    #saved as we need the rho at the end
    originalLines = lines
    
    #remove rho from line array as we don't need it for cluster
    #thetaArray is nxmxj, n is number of lines and n is column 
    thetaArray = np.delete(lines,[0],2)

    #8x1
    thetaArray = np.reshape(thetaArray,(7,1))
    thetaArray = np.float32(thetaArray)
    
    # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
    #criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)\
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)

    # Set flags 
    flags = cv2.KMEANS_RANDOM_CENTERS

    # Apply KMeans
    compactness,labels,centers = cv2.kmeans(thetaArray,2,None,criteria,10,flags)
    a = thetaArray[labels==0]
    b = thetaArray[labels==1]
    
   
    #Get majority cluster
    if np.count_nonzero(a) > np.count_nonzero(b):
        originalLines = originalLines[labels==0]
    else:
        originalLines = originalLines[labels==1]
    
    #sort by highest rho value first (lowest string first)
    sortedLines = originalLines[originalLines[:,0].argsort()]
    return sortedLines


"""
Get the intensity profile of a line
line: [(start_x,start_y), (end_x,end_y)]
"""
def bresenham_march(img, line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    #tests if any coordinate is outside the image
    if ( 
        x1 >= img.shape[0]
        or x2 >= img.shape[0]
        or y1 >= img.shape[1]
        or y2 >= img.shape[1]
    ): #tests if line is in image, necessary because some part of the line must be inside, it respects the case that the two points are outside
        if not cv2.clipLine((0, 0, *img.shape[:2]), line[0], line[1]):
            print("not in region")
            return

    steep = math.fabs(y2 - y1) > math.fabs(x2 - x1)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # takes left to right
    also_steep = x1 > x2
    if also_steep:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = math.fabs(y2 - y1)
    error = 0.0
    delta_error = 0.0
    # Default if dx is zero
    if dx != 0:
        delta_error = math.fabs(dy / dx)

    y_step = 1 if y1 < y2 else -1

    y = y1
    ret = []
    for x in range(x1, x2):
        p = (y, x) if steep else (x, y)
        if p[0] < img.shape[0] and p[1] < img.shape[1] and p[1] > 0:
        
            ret.append((p, img[p]))
        error += delta_error
        if error >= 0.5:
            y += y_step
            error -= 1
    if also_steep:  # because we took the left to right instead
        ret.reverse()
    return ret
    
    
        
 









    

    
    
    
    
    
    
    
    
    
    
    
 


        
        
    





        
        
        