import cv2
import time
import filters
import houghProcessing
import guitar
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
        
        frameNumber = 0 #count every 10 frames 0-9
    
        
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            greyFrame = filters.applyGaussianBlur(greyFrame)
            
        
            if frame is not None:
                if frameNumber == 0: #only update new strings every 3 frames
                    """Prepare the frame for line detection"""
                    gaussianFiltered = filters.applyGaussianBlur(frame)
                    edges = filters.autoCannyEdge(gaussianFiltered)
        
                    """Get the string lines"""
                    rawStringLines = houghProcessing.getHoughLines(edges)
                
                    """Process string lines"""
                    processedStringLines = houghProcessing.processStringLinesByKmeans(rawStringLines)
                    stringLinePoints = houghProcessing.getStringLinePoints(processedStringLines)
                    # if stringLinePoints is not None:
                    #     for lines in stringLinePoints:
                    #         if count == 0:
                    #             lineIntensity = houghProcessing .bresenham_march(greyFrame,lines)
                    #             #for intensity in lineIntensity:
                    #               #print(intensity[1], intensity[0])    
                
                    """Update the guitar object with new string coordinates if fully detected on this frame""" 
                    if stringLinePoints and len(stringLinePoints) == 6: #possibly detected all strings successfully   
                        currentGuitar.setStringPoints(stringLinePoints)
                      
                    

                """Update video frame that the user will see"""
                frame = currentGuitar.drawString(frame)
                self._captureManager.frame = frame
                frameNumber += 1
                if frameNumber == 3:
                    frameNumber = 0
                pass

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