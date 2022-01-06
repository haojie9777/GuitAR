import cv2
import numpy as np
import math
import houghProcessing
from collections import defaultdict
"""
class to represent a guitar object and information about its string and frets.

stringCoordinates: dictionary containing start and end coordinates of 6 strings
and 2 outer edges of fretboard
e.g: stringPoints[0] = [(1,2), (3,4)]

stringPoints: dictionary containing (rho and theta) tuple of 6 strings
and 2 outer edges of fretboard
e.g: stringLines[0] = upper edge of fretboard
     stringLines[1] = string 1
     ...
     stringLines[7] = lower edge of fretboard

fretPoints: list containing tuples of start and end point of line denoting a fret
e.g fretPoints[0] = [(1,2),(3,4)] we store fret 0 to fret 5's coordinates

chords: dictionary containing position of chords in terms of string and fret
chords["c"] = [(2,3), (4,2), (5,1)]-> first note is on string 2 and mid pt of fret 2 and 3

"""
class Guitar():
    
    def __init__(self):
        self.stringCoordinates = defaultdict(lambda: None)
        self.stringPoints = defaultdict(lambda: None)
        self.fretCoordinates = defaultdict(lambda: None)
        self.chords = defaultdict(lambda: None)

        
        #initialize chords
        self.chords["c"] = [(2,3), (4,2), (5,1)]
        self.chords["d"] = [(4,2), (5,3),(6,2)]
        
        #indicate whether inital full string detection is carried out or not
        self.initialStringsFullyDetected = False 
        self.initialFretsFullyDetected = False
        
    def getStringCoordinates(self):
        return self.stringCoordinates
    
    def setStringCoordinates(self, coordinates):
        if coordinates is None:
            return
        if len(coordinates) == 8: #Successfully detect all 8 lines in this frame
            for i in range(8):
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
        #Successfully detect all 8 lines in this frame, 6 strings + top and bottom of fretboard
        if len(points) == 8: 
            for i in range(8):
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
                    if abs(rho - self.stringPoints[i][0]) <= 0.5:
                        #update this string's rho and theta
                        self.stringPoints[i] = (rho,theta)
                       
                #store as coordinates
                coordinates = houghProcessing.getStringLineCoordinates(self.stringPoints)
                self.setStringCoordinates(coordinates)
     
            return
    
    def getFretCoordinates(self):
        return self.fretPoints
       
    """Store detected frets' coordinates, from fret 0 to fret 5"""
    def setFretCoordinates(self, coordinates):
        if coordinates is None:
            return
        if len(coordinates) >= 6 and not self.initialFretsFullyDetected: #sufficient number of frets detected
            for i,fret in enumerate(coordinates[0:6]):
                self.fretCoordinates[i] = fret #store fret 0 to fret 5's coordinates
            self.initialFretsFullyDetected = True
            return
        elif len(coordinates) >= 6 and self.initialFretsFullyDetected: #update position from prev frame if close in x coordinate
            for i,fret in enumerate(coordinates[0:6]):
                if abs(fret[0] - self.fretCoordinates[i][0]) < 40:
                    self.fretCoordinates[i] = fret
            return

    
    """Display frets of the guitar in the frame"""
    def drawFrets(self,frame):
        if self.fretCoordinates is not None:
            for i in range(0, len(self.fretCoordinates)):
                l = self.fretCoordinates[i]
                cv2.line(frame, (l[0], l[1]), (l[2],l[3]), (0,0,255), 2, cv2.LINE_AA)
        return
    
        
    
    def drawString(self,frame):
        for i in range(len(self.stringCoordinates)):
            if self.stringCoordinates[i] is not None:
                if i != 0 and i != 7:
                    pt1 = self.stringCoordinates[i][0]
                    pt2 = self.stringCoordinates[i][1]
                    #draw line on string
                    cv2.line(frame, pt1, pt2, (0,255,0),1,cv2.LINE_AA)
                
        return frame
    
    def drawStringGivenCoordinates(self,frame,points):
        if points is None:
            return frame
        for i in range(len(points)):
            pt1 = points[i][0]
            pt2 = points[i][1]
            #draw line on string
            cv2.line(frame, pt1, pt2, (0,255,0),1,cv2.LINE_AA)
        return frame
    

    """
    Get the bounding box containing the first 5 frets of the fretboard, for fret detection
    """
    def getFretboardBoundingBoxPoints(self):
        #need to wait for first and sixth strings to be detected properly first
        if not self.initialStringsFullyDetected:
            return None
        #define 4 corners of bounding box
        p1 = list(self.stringCoordinates[1][0])
        #offset to make bounding box slightly bigger than fretboard
        p1[1] -= 15
        p1[0] -= 60
        p2 = list(self.stringCoordinates[6][0])
        p2[1] += 40
        p2[0] -= 50
        p3 = list(self.stringCoordinates[6][1])
        p3[0] -= 100
        p3[1] += 70
        p4 = list(self.stringCoordinates[1][1])
        p4[0] -= 100
        p4[1] += 0
        
        return [p1,p2,p3,p4]
    
      
    def line(self,p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C

    """
    Find intersection of two lines using crammer's rule
    """
    def intersection(self,L1, L2):
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return x,y
        else:
            return False
    
    """
    Draws circles representing notes of a chord
    """
    def showChord(self,frame,chord):
        #can't show chord since insufficient information
        if not self.initialFretsFullyDetected or not self.initialStringsFullyDetected:
            return frame
        #retrieve chord fingering information
        chordInformation = self.chords[chord]
        
        
        #alternate color for every note
        #noteColour = {0:(0,0,255), 1 :(0,255,0), 2:(255,0,0)}
       
        #display each note of chord
        for i,note in enumerate(chordInformation):
            
            #get string line coordinates
            p1 = list(self.stringCoordinates[note[0]][0])
            p2 = list(self.stringCoordinates[note[0]][1])
            string = self.line(p1,p2)
            
            #get higher fret line coordinates
            p1 = list(self.fretCoordinates[note[1]][0:2])
            p2 = list(self.fretCoordinates[note[1]][2:4])
            higherFret = self.line(p1,p2)
            
            R1 = (self.intersection(string, higherFret))
            x1,y1 = R1
            x1 = int(x1)
            y1 = int(y1)
            
            #get lower fret line coordinates
            p1 = list(self.fretCoordinates[note[1]-1][0:2])
            p2 = list(self.fretCoordinates[note[1]-1][2:4])
            lowerFret = self.line(p1,p2)
            
            R2 = (self.intersection(string, lowerFret))
            x2,y2 = R2
            x2 = int(x2)
            y2 = int(y2)
           
            if R1 and R2: # Note is mid point of the intersection of both frets with the string
                #color = noteColour[(i%3)]
                color = (255,0,255)
                x = int((x1 + x2) /2)
                y = int((y1 + y2) /2)
                cv2.circle(frame,(x,y), 5, color, -1)
       
                    

                
                
            
        
        
        
        
        
        
        
    
    
    
    
   
        
        
        
        
        
        
        
    
    
   