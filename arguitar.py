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
        
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            
        
            if frame is not None:
                """Prepare the frame for line detection"""
                gaussianFiltered = filters.applyGaussianBlur(frame)
                edges = filters.autoCannyEdge(gaussianFiltered)
    
                """Get the string lines """
                rawStringLines = houghProcessing.getHoughLines(edges)
            
                """Process string lines"""
                processedStringLines = houghProcessing.processStringLinesByKmeans(rawStringLines)
                stringLinePoints = houghProcessing.getStringLinePoints(processedStringLines)
                
                """Update the guitar object"""
                currentGuitar.setStringPoints(stringLinePoints)
                #print(currentGuitar.getStringPoints())
                frame = houghProcessing.drawStrings(processedStringLines,frame)
                
            
                """Update video frame that the user will see"""
                self._captureManager.frame = frame
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