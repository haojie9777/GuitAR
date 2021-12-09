import cv2
import time
import filters
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
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            
        
            if frame is not None:
                #do image processing
                
                # 1.blur/averaging filter
                gaussianFiltered = filters.applyGaussianBlur(frame)
                #medianBlurred = filters.applyMedianBlur(frame)
                #thresh = filters.applyThreshold(gaussianFiltered)
                
                # 2.Canny edge detection
                edges = filters.autoCannyEdge(gaussianFiltered)
             
                
                # 3.Dilation to enlarge edges
                #edges = filters.applyDilation(edges)
                #erodedFrame = filters.applyErosion(gaussianFiltered)
                edges = filters.applyOpening(edges)
                
    
             

                
                #3.5 sobel filters to accentuate vertical/horizontal edges
                #verticalEdges = filters.applySobelX(edges)
                # horizontalEdges = filters.applySobelY(edges)
                
    
                # 4.Get raw houghLines lines
                #frame = filters.applyHoughLines(edges, frame)
                #frame = filters.applyHoughLines(thresh, frame)
                #frame = filters.applyHoughLinesP(edges, frame)
                
            
                #process vertical lines to get frets
                #unprocessedLines = filters.getHoughLinesP(verticalEdges, frame)
                
                
                # 5. process liness
                
                # 2 stages of line detection, 1 for strings(horizontal) and 1 for frets (vertical)
            
        
               #add final image to display
                self._captureManager.frame = edges
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