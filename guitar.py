import cv2
import numpy as np
import math
import houghProcessing
from collections import defaultdict
"""
class to represent a guitar object and information about its string and frets.

stringCoordinates: dictionary containing start and end coordinates of 6 strings
e.g: stringPoints[0] = [(1,2), (3,4)]

stringPoints: dictionary containing (rho and theta) tuple of 6 strings
e.g: stringLines[0] = (rho, theta)

fretPoints: list containing tuples of start and end point of line denoting a fret
e.g fretPoints[1] = [(1,2),(3,4)]
"""
class Guitar():
    
    def __init__(self):
        self.stringCoordinates = defaultdict(lambda: None)
        self.stringPoints = defaultdict(lambda: None)
        self.fretPoints = defaultdict(lambda: None)

        #indicate whether inital full string detection is carried out or not
        self.initialStringsFullyDetected = False 
        self.initialFretsFullyDetected = False
        
    def getStringCoordinates(self):
        return self.stringCoordinates
    
    def setStringCoordinates(self, coordinates):
        if coordinates is None:
            return
        if len(coordinates) == 6: #Successfully detect all 6 lines in this frame
            for i in range(6):
                #first line is string 1 (top string)
                self.stringCoordinates[i] = coordinates[i]
            self.initialStringsFullyDetected = True
        
        return
        # else: #some strings undetected, need to use detected ones from previous frames
      
    
    def getStringPoints(self):
        return self.stringPoints
    
    """ 
    updates the (rho,theta) points for every string if it is close to prev frame's value
    """
    def setStringPoints(self, points):
        if points is None:
            return
        #Successfully detect all 6 lines in this frame
        if len(points) == 6: 
            for i in range(6):
                self.stringPoints[i] = points[i]
            self.initialStringsFullyDetected = True
            #save coordinates of strings for this frame
            coordinates = houghProcessing.getStringLineCoordinates(points)
            self.setStringCoordinates(coordinates)
            return
        #some string not detected, need to check if current frame values close to prev frame
        else: 
            #proceed only if all 6 strings detected successfully beforehand
            if self.initialStringsFullyDetected:
                for i, (rho, theta) in enumerate(points):
                     #this string's points close to pre frame's one, likely detected correctly
                    if abs(rho - self.stringPoints[i][0]) < 2:
                        #update this string's rho and theta
                        self.stringPoints[i] = (rho,theta)
                
                #store as coordinates
                coordinates = houghProcessing.getStringLineCoordinates(self.stringPoints)
                self.setStringCoordinates(coordinates)
            return
                
            
    
    
    def getFretPoints(self):
        return self.fretPoints
       
    def setFretPoints(self, fretNumber, points):
        self.fretPoints[fretNumber] = points
        return
    
    def drawString(self,frame):
        for i in range(6):
            if self.stringCoordinates[i] is not None:
                pt1 = self.stringCoordinates[i][0]
                pt2 = self.stringCoordinates[i][1]
                
                #draw line on string
                cv2.line(frame, pt1, pt2, (0,255,0),1,cv2.LINE_AA)
                
                # #label string number
                # stringNumber = str(i + 1)+ ""
                # frame = cv2.putText(frame,stringNumber, pt1, \
                #     cv2.FONT_HERSHEY_SIMPLEX, 1, 
                #  (0,0,255), 2, cv2.LINE_AA, False)
        return frame
    
    def drawStringGivenCoordinates(self,frame,points):
        if points is None:
            return frame
        for i in range(len(points)):
            pt1 = points[i][0]
            pt2 = points[i][1]
            
            #draw line on string
            cv2.line(frame, pt1, pt2, (0,255,0),1,cv2.LINE_AA)
            
            # #label string number
            # stringNumber = str(i + 1)+ ""
            # frame = cv2.putText(frame,stringNumber, pt1, \
            #     cv2.FONT_HERSHEY_SIMPLEX, 1, 
            #     (0,0,255), 2, cv2.LINE_AA, False)
        return frame
    

    """
    Get the bounding box containing the first 5 frets of the fretboard, for fret detection
    """
    def getFretboardBoundingBoxPoints(self):
        #need to wait for first and sixth strings to be detected properly first
        if not self.initialStringsFullyDetected:
            return None
        #define 4 corners of bounding box
        p1 = list(self.stringCoordinates[0][0])
        #offset to make bounding box slightly bigger than fretboard
        p1[1] -= 15
        p1[0] -= 80
        p2 = list(self.stringCoordinates[5][0])
        p2[1] += 40
        p2[0] -= 65
        p3 = list(self.stringCoordinates[5][1])
        p3[0] -= 100
        p3[1] += 70
        p4 = list(self.stringCoordinates[0][1])
        p4[0] -= 100
        p4[1] += 0
        
        #print(p1,p2,p3,p4)
 
        return [p1,p2,p3,p4]
        
        
        
        
        
        
    
    
   