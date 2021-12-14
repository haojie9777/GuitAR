import cv2
import numpy as np
import math
from collections import defaultdict
'''
class to represent a guitar object and information about its string and frets.

stringPoints: dictionary containing start and end coordinates of 6 strings
e.g: stringPoints[1] = [(1,2), (3,4)]

fretPoints: list containing tuples of start and end point of line denoting a fret
e.g fretPoints[1] = [(1,2),(3,4)]
'''
class Guitar():
    
    def __init__(self):
        self.stringPoints = defaultdict(None)
        self.fretPoints = defaultdict(None)
        
    def getStringPoints(self):
        return self.stringPoints
    
    def getFretPoints(self):
        return self.fretPoints
    
    def setStringPoints(self, stringNumber, points):
        self.stringPoints[stringNumber] = points
    
    
    def setFretPoints(self, fretNumber, points):
        self.fretPoints[fretNumber] = points
        
    

        

    
        