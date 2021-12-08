
import cv2
class Guitar():
    
    def __init__(self):
        self.stringPoints = [[] for i in range(6)]
        self.fretPoints = [[] for i in range(5)]
        
    
    # def processLines(lines):
    #     if lines is None:
    #         return
    #     for line in lines:
    #         if lines
            
    
        
    def kMeansLines(self, lines):
        if lines is None:
            return
        # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        # Set flags (Just to avoid line break in the code)
        flags = cv2.KMEANS_RANDOM_CENTERS
        # Apply KMeans
        compactness,labels,centers = cv2.kmeans(lines,2,None,criteria,10,flags)
        return centers
        
        
    
        