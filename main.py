import cv2
import time
import filters
import houghProcessing
import guitar
import numpy as np
from managers import WindowManager, CaptureManager

class ARGuitar(object):

    def __init__(self):
        self._windowManager = WindowManager('ARGuitar',
                                            self.onKeypress)
        capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self._captureManager = CaptureManager(
            capture, self._windowManager, True)

    def run(self):
        """Run the main loop."""
        self._windowManager.createWindow()
        
        """Holds information about the guitar"""
        currentGuitar = guitar.Guitar()
        
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            
            if frame is not None:
                
                maskFrame = np.zeros(frame.shape[:2], dtype="uint8")
         
                """Extract edges from frame for line detection"""
                #restrict the area to search for guitar strings, to avoid curve string interference from guitar neck
                roiFrame = frame[:,0:440]
                gaussianFiltered = filters.applyGaussianBlur(roiFrame)
                edges = filters.autoCannyEdge(gaussianFiltered) 
               
                """Get the string lines"""
                rawStringLines = houghProcessing.getHoughLines(edges)
              
                """Process string lines and get (rho,theta) points of strings"""
                #(rho, theta) of strings
                rhoThetaStrings = houghProcessing.convertNpToListForStrings(rawStringLines)
                """Update the guitar object with new string points""" 
                if rhoThetaStrings:  
                    currentGuitar.setStringPoints(rhoThetaStrings)
                
                """Draw bounding box on fretboard and use it for a mask"""
                if currentGuitar.getFretboardBoundingBoxPoints():
                    pts = np.array(currentGuitar.getFretboardBoundingBoxPoints(),np.int32)
                    pts = pts.reshape((-1,1,2))
                    cv2.polylines(frame,[pts],True,(0,255,255),2, cv2.LINE_AA)
                
                    
                    """create mask on fretboard to perform fret detection"""
                    cv2.fillConvexPoly(maskFrame,pts,(255,255,255))
                    masked = cv2.bitwise_and(frame, frame, mask=maskFrame)
                    masked = filters.applyThreshold(masked, "manual")
                    masked = filters.applySobelX(masked)
                    
                    """ Extract fret lines segments"""
                    rawFretLines = houghProcessing.getHoughLinesP(masked)
                    processedFretLines = houghProcessing.processFretLines(rawFretLines)
        
                    """Update the guitar object with new fret coordinates""" 
                    currentGuitar.setFretCoordinates(processedFretLines)
                    currentGuitar.drawFrets(frame)
        
                
                """Update video frame that the user will see"""
                currentGuitar.drawString(frame)
                currentGuitar.showChord(frame,"c")
                self._captureManager.frame = frame
        

            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onKeypress(self, keycode):
        """Handle a keypress.
        space  -> Take a screenshot.
        tab    -> Start/stop recording.
        escape -> Quit.
        """
        if keycode == 32: # space
            self._captureManager.writeImage('{}.png'.format(time.strftime("%Y%m%d-%H%M%S")))
            print("Took a screenshot")
        elif keycode == 9: # tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo(
                    'recording.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27: # escape
            self._windowManager.destroyWindow()

if __name__=="__main__":
    ARGuitar().run()
    
    
'''  Unused stuff
         3.Dilation to enlarge edges
                #dilated = filters.applyDilation(thresh)
                #eroded = filters.applyErosion(gaussianFiltered)
                #3.5 sobel filters to accentuate vertical/horizontal edges
                #verticalEdges = filters.applySobelX(edges)
                # horizontalEdges = filters.applySobelY(edges)
'''