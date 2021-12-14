import cv2
import numpy as np
import math
from collections import defaultdict
"""
class to represent a guitar object and information about its string and frets.

stringPoints: dictionary containing start and end coordinates of 6 strings
e.g: stringPoints[1] = [(1,2), (3,4)]

fretPoints: list containing tuples of start and end point of line denoting a fret
e.g fretPoints[1] = [(1,2),(3,4)]
"""
class Guitar():
    
    def __init__(self):
        self.stringPoints = defaultdict(None)
        self.fretPoints = defaultdict(None)
        self.initialStringsDetected = False #indica
        
    def getStringPoints(self):
        return self.stringPoints
    
    def getFretPoints(self):
        return self.fretPoints
    
    def setStringPoints(self, points):
        if points is None:
            return
        if len(points) == 6: #Successfully detect all 6 lines
            for i in range(1,7):
                self.stringPoints[i] = points[i-1]
            if not self.initialStringsDetected:
                self.initialStringsDetected = True
            return

    def setFretPoints(self, fretNumber, points):
        self.fretPoints[fretNumber] = points
        return
    
    def drawString(frame):
        return