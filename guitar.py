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
e.g fretPoints[0] = [(1,2),(3,4)] we store fret 0 to fret 5's coordinates

chords: dictionary containing position of chords in terms of string and fret
chords["c"] = [(1,3), (3,2), (4,1)]

"""
class Guitar():
    
    def __init__(self):
        self.stringCoordinates = defaultdict(lambda: None)
        self.stringPoints = defaultdict(lambda: None)
        self.fretCoordinates = defaultdict(lambda: None)
        self.chords = defaultdict(lambda: None)

        
        #initialize chords
        self.chords["c"] = [(2,3), (4,2), (5,1)]
        
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
                
            
    
    
    def getFretCoordinates(self):
        return self.fretPoints
       
    """Store detected frets' coordinates. The first line detected is usually fret 0, and will
    be ignored. The next 5 lines will be stored as the first 5 frets"""
    def setFretCoordinates(self, coordinates):
        if coordinates is None:
            return
        if len(coordinates) >= 6: #sufficient number of frets detected
            for i,fret in enumerate(coordinates[0:6]):
                self.fretCoordinates[i] = fret #store fret 0 to fret 5's coordinates
                self.initialFretsFullyDetected = True
        #some frets not detected, need to check if current frame values close to prev frame
        else:
            if self.initialFretsFullyDetected:
                for i,fret in enumerate(coordinates[0:6]):
                    #update fret position if close to prev frame's position
                    if abs(fret[0] - self.fretCoordinates[i][0]) < 2:
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
        for i in range(6):
            if self.stringCoordinates[i] is not None:
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
        p1 = list(self.stringCoordinates[0][0])
        #offset to make bounding box slightly bigger than fretboard
        p1[1] -= 15
        p1[0] -= 60
        p2 = list(self.stringCoordinates[5][0])
        p2[1] += 40
        p2[0] -= 50
        p3 = list(self.stringCoordinates[5][1])
        p3[0] -= 100
        p3[1] += 70
        p4 = list(self.stringCoordinates[0][1])
        p4[0] -= 100
        p4[1] += 0
    
        return [p1,p2,p3,p4]
    
      
    def line(self,p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C

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
        for i,note in enumerate(chordInformation):
            
            p1 = list(self.stringCoordinates[note[0]][0])
            p2 = list(self.stringCoordinates[note[0]][1])
            string = self.line(p1,p2)
            
            p1 = list(self.fretCoordinates[note[1]][0:2])
            p2 = list(self.fretCoordinates[note[1]][2:4])
            higherFret = self.line(p1,p2)
            
            R = (self.intersection(string, higherFret))
            x,y = R
            x = int(x)
            y = int(y)
           
            if R:
                print("Intersection detected:", R)
                cv2.circle(frame,(x,y), 5, (255,0,0), -1)
            else:
                print("No single intersection point detected")
                    
    
    
                
                
            
        
        
        
        
        
        
        
    
    
    
    
   
        
        
        
        
        
        
        
    
    
   