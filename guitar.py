import cv2
import numpy as np
import math
import houghTransform
from collections import defaultdict
"""
class to represent a guitar object and information about its string and frets.

stringCoordinates: dictionary containing start and end coordinates of 6 strings
and 2 outer edges of fretboard
e.g: stringPoints[0] = [(1,2), (3,4)]

stringPoints: dictionary containing (rho and theta) tuple of 6 strings
and 2 outer edges of fretboard
e.g: stringLines[0] = string 1
     stringLines[1] = string 2
     ...
     stringLines[5] = string 6

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
        self.chords["c"] = [(1,3), (3,2), (4,1)]
        self.chords["d"] = [(3,2), (4,3),(5,2)]
        self.chords["g"] = [(0,3), (1,2), (5,3)]
        self.chords["em"] = [(1,2), (2,2)]
        
        #indicate whether inital full string detection is carried out or not
        self.initialStringsFullyDetected = False 
        self.initialFretsFullyDetected = False
        
    def getStringCoordinates(self):
        return self.stringCoordinates
    
    def setStringCoordinates(self, coordinates):
        if coordinates is None:
            return
        if len(coordinates) == 6: #Successfully detect all 6 strings in this frame
            for i in range(6):
                #first line is string 1 (top string)
                self.stringCoordinates[i] = coordinates[i]
            self.initialStringsFullyDetected = True
        
        return
        # else: #some strings undetected, need to use detected ones from previous frames
      
    
    def getStringPoints(self):
        return self.stringPoints
    
        
    
    #updates the (rho,theta) points for every string
    def setStringPoints(self, points):
        if points is None:
                return
        #detected 7 lines -> assumed to be bottom edge line + bottom 5 strings + top edge line
        #print(len(points))
        if len(points) == 7:
            #first line is top edge
            for i in range(1,5): #store middle 4 strings
                self.stringPoints[i] = points[i] #2,3,4,5th strings saved
                
            #extrapolate for first and sixth strings rho and theta
            dif = self.stringPoints[2][0] - self.stringPoints[1][0]
            rho = self.stringPoints[1][0] - dif
            theta = self.stringPoints[1][1]
            self.stringPoints[0] = (rho, theta)
        
            dif = self.stringPoints[4][0] - self.stringPoints[3][0]
            rho = self.stringPoints[4][0] + dif
            theta = self.stringPoints[4][1]
            self.stringPoints[5] = (rho, theta)
            
            self.initialStringsFullyDetected = True
            
            coordinates = houghTransform.getStringLineCoordinates(self.stringPoints)
            self.setStringCoordinates(coordinates)
            return
        # elif len(points) == 8:
        #        #first line is top edge
        #     for i in range(2,6): #store middle 4 strings
        #         self.stringPoints[i-1] = points[i] #2,3,4,5th strings saved
                
        #     #extrapolate for first and sixth strings rho and theta
        #     dif = self.stringPoints[2][0] - self.stringPoints[1][0]
        #     rho = self.stringPoints[1][0] - dif
        #     theta = self.stringPoints[1][1]
        #     self.stringPoints[0] = (rho, theta)
        
        #     dif = self.stringPoints[4][0] - self.stringPoints[3][0]
        #     rho = self.stringPoints[4][0] + dif
        #     theta = self.stringPoints[4][1]
        #     self.stringPoints[5] = (rho, theta)
            
        #     self.initialStringsFullyDetected = True
            
        #     coordinates = houghTransform.getStringLineCoordinates(self.stringPoints)
        #     self.setStringCoordinates(coordinates)
        #     return
     
    
    def getFretCoordinates(self):
        return self.fretPoints
       

    """Store detected frets' coordinates, from fret 0 to fret 5"""
    def setFretCoordinates(self, coordinates):
        if coordinates is None:
            return
        if len(coordinates) >= 5 and not self.initialFretsFullyDetected: #sufficient number of frets detected
            #determine if inital set of coordinates have similar x distance between them. Else, probably bad detection and reject
            gap = abs(coordinates[0][0]-coordinates[1][0])
            for i in range(1,len(coordinates)-1):
                if  gap -10 <= abs(coordinates[i][0] - coordinates[i+1][0]) <= gap + 10:
                    gap = abs(coordinates[i][0]-coordinates[i+1][0])
                else:
                    return
            print("fret coordinates good for inital detection")
            for i,fret in enumerate(coordinates[0:5]):
                self.fretCoordinates[i] = fret #store fret 0 to fret 4's coordinates
            self.initialFretsFullyDetected = True
        elif len(coordinates) >= 6 and self.initialFretsFullyDetected:
             for i,fret in enumerate(coordinates[0:5]):
                if abs(fret[0] - self.fretCoordinates[i][0]) <= 10: #update position only if too far
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
                pt1 = self.stringCoordinates[i][0]
                pt2 = self.stringCoordinates[i][1]
                #draw line on string
                cv2.line(frame, pt1, pt2, (0,255,0),2,cv2.LINE_AA)
            
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
    


    #Get the bounding box containing the first 5 frets of the fretboard, for fret detection
    def getFretboardBoundingBoxPoints(self, offset = True):
        #need to wait for first and sixth strings to be detected properly first
        if not self.initialStringsFullyDetected:
            return None
        #define 4 corners of bounding box
        #offset = True -> scale to make bounding box slightly bigger than fretboard
        if offset:
            p1 = list(self.stringCoordinates[0][0])
            p1[1] -= 10
            p1[0] -= 70
            
            p2 = list(self.stringCoordinates[5][0])
            p2[1] += 60
            p2[0] -= 40
        
            p3 = list(self.stringCoordinates[5][1])
            p3[1] += 50
        
            p4 = list(self.stringCoordinates[0][1])
            p4[1] -= 30
        #no offset
        else:
            p1 = list(self.stringCoordinates[0][0])
            p2 = list(self.stringCoordinates[5][0])
            p3 = list(self.stringCoordinates[5][1])
            p4 = list(self.stringCoordinates[0][1])
             
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
    
    
    #Draws circles representing notes of a chord
    def showChord(self,frame,chord):
        #can't show chord since insufficient information
        if not self.initialFretsFullyDetected or not self.initialStringsFullyDetected:
            return frame
        #retrieve chord fingering information
        chordInformation = self.chords[chord]
      
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
                color = (255,0,255)
                x = int((x1 + x2) /2)
                y = int((y1 + y2) /2)
                cv2.circle(frame,(x,y), 5, color, -1)
       
                    

                
                
            
        
        
        
        
        
        
        
    
    
    
    
   
        
        
        
        
        
        
        
    
    
   