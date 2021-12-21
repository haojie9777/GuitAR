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
        self.initialStringsDetected = False 
        
    def getStringCoordinates(self):
        return self.stringCoordinates
    
    def setStringCoordinates(self, coordinates):
        if coordinates is None:
            return
        if len(coordinates) == 6: #Successfully detect all 6 lines in this frame
            for i in range(6):
                #first line is string 1 (top string)
                self.stringCoordinates[i] = coordinates[i]
            self.initialStringsDetected = True
        
        return
        # else: #some strings undetected, need to use detected ones from previous frames
      
    
    def getStringPoints(self):
        return self.stringPoints
    
    """ 
    updates the (rho,theta) points for every string
    uses the rho distance between adjacent string 15-28
    to determine if an adjacent string is not detected in current frame, and use prev frame value to fill in
    """
    def setStringPoints(self, points):
        if points is None:
            return
        if len(points) == 6: #Successfully detect all 6 lines in this frame
            for i in range(6):
                self.stringPoints[i] = points[i]
            self.initialStringsDetected = True
            #save coordinates of strings for this frame
            coordinates = houghProcessing.getStringLineCoordinates(points)
            self.setStringCoordinates(coordinates)
            return
        else: #some string
            print("one iteration")
            for rho, theta in points:
                print(rho,theta)
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
    
    
   