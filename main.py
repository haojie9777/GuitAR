import cv2
import time
import filters
import houghTransform
import skinDetector
import guitar
import numpy as np
import winsound
from managers import WindowManager, CaptureManager


class ARGuitar(object):

    def __init__(self):
        self._windowManager = WindowManager('ARGuitar',
                                            self.onKeypress)
        capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self._captureManager = CaptureManager(
            capture, self._windowManager, False)
        
        #Holds information about the guitar
        self._currentGuitar = guitar.Guitar()
        
        #Hold information about finger occlusion
        self._skinDetector = skinDetector.SkinDetector()
        
        #decide whether to show a chord
        self._chordToShow = None
        
        #Indicate whether the player's fingers are blocking the frets
        self._occluded = False
        
    def run(self):
        """Run the main loop."""
        self._windowManager.createWindow()
        
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            
            if frame is not None:
                """Create a mask for later steps"""
                maskFrame = np.zeros(frame.shape[:2], dtype="uint8")
                
                """Extract edges from frame for line detection"""
                #restrict the area to search for guitar strings, to avoid curve string interference from guitar neck
                roiFrame = frame[:,0:440]
                roiFrame = frame
                gaussianFiltered = filters.applyGaussianBlur(roiFrame)
                thresholdedFrame = filters.applyThreshold(gaussianFiltered,"adaptive")
             
                """Get the string lines"""
                rawStringLines = houghTransform.getHoughLines(thresholdedFrame)
                
                # frame = houghTransform.applyHoughLines(thresholdedFrame, frame)
            
                """Process string lines and get (rho,theta) points of strings"""
                #(rho, theta) of strings
                rhoThetaStrings = houghTransform.convertNpToListForStrings(rawStringLines)
                """Update the guitar object with new string points""" 
                if rhoThetaStrings:  
                    self._currentGuitar.setStringPoints(rhoThetaStrings)
                
                """Draw bounding box on fretboard and use it for a mask"""
                if self._currentGuitar.getFretboardBoundingBoxPoints(offset=True):
                    pts = np.array(self._currentGuitar.getFretboardBoundingBoxPoints(),np.int32)
                    pts = pts.reshape((-1,1,2))
                    cv2.polylines(frame,[pts],True,(0,255,255),2, cv2.LINE_AA)
                    
                    """create mask on fretboard to perform fret detection"""
                    cv2.fillConvexPoly(maskFrame,pts,(255,255,255))
                    masked = cv2.bitwise_and(frame, frame, mask=maskFrame)
                    masked = filters.applyThreshold(masked,"manual","fret")
                    masked = filters.applyDilation(masked)
                    masked = filters.applyErosion(masked)
                    masked = filters.applySobelX(masked)
            
                    """ Extract fret lines segments"""
                    rawFretLines = houghTransform.getHoughLinesP(masked)
                    processedFretLines = houghTransform.processFretLines(rawFretLines)
                  
                    
                
                """Detect if fingers covering the fretboard"""
                if self._currentGuitar.getFretboardBoundingBoxPoints(offset =False):
                    pts = np.array(self._currentGuitar.getFretboardBoundingBoxPoints(offset = False),np.int32)
                    pts = pts.reshape((-1,1,2))
                    skinFrame = cv2.bitwise_and(frame, frame, mask=maskFrame)
                    if not self._skinDetector.isSkinDetected(skinFrame) or not self._currentGuitar.initialFretsFullyDetected:
                        """Update the guitar object with new fret coordinates only when no finger occlusion""" 
                        self._currentGuitar.setFretCoordinates(processedFretLines)
                        self._occluded = False
                        #self._currentGuitar.drawFrets(frame)
                    else:
                        print("finger occlusion detected")
                        self._occluded = True
             
                
                """Draw strings and show chord"""
                self._currentGuitar.drawString(frame)
                if self._chordToShow:
                    self._currentGuitar.showChord(frame,self._chordToShow)
        
                    
                """Reversed the frame and write text if needed"""
                frame = np.fliplr(frame)
                frame = frame.copy()
                # for idx,pts in self._currentGuitar.getStringCoordinates().items():
                #     #account for flip
                #     correctedPt = (640 -pts[0][0],pts[0][1])
                #     cv2.putText(frame,str(6-idx),correctedPt,\
                #         cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2,cv2.LINE_AA)
                if self._chordToShow:
                    chordText = self._chordToShow.upper()
                    cv2.putText(frame, chordText, (250,150),\
                        cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0), 2, cv2.LINE_AA)
                    
                """if calibration of fret and string successful, indicate on the frame"""
                if self._currentGuitar.initialStringsFullyDetected and self._currentGuitar.initialFretsFullyDetected:
                    cv2.putText(frame, "Calibration Successful", (200,450),\
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                
                """indicate if user's fingers are blocking the fretboard, causing poor detection"""
                if self._occluded:
                    cv2.putText(frame, "Fretboard Occluded", (400,450),\
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                    
                """Update video frame that the user will see"""
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
        elif keycode == 99: #show c chord
            self._chordToShow = "c"
            winsound.PlaySound('sounds/C.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
        elif keycode == 100: #show d chord
            self._chordToShow = "d"
            winsound.PlaySound('sounds/D.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
        elif keycode == 101: #show d chord
            self._chordToShow = "em"
            winsound.PlaySound('sounds/Em.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
        elif keycode == 103: #show d chord
            self._chordToShow = "g"
            winsound.PlaySound('sounds/G.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
        #play chord sequence of c,d,g,em

if __name__=="__main__":
    ARGuitar().run()
    