import cv2
import time
import numpy
import filters
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
                #bilateralFilteredFrame = filters.applyBilateralFilter(frame)
                gaussianFiltered = filters.applyGaussianBlur(frame)
                
                # 2.Canny edge detection
                edges = filters.getCannyEdge(gaussianFiltered)
                
                # 3.Dilation to enlarge edges
                edges = filters.applyDilation(edges)
                
                blurredEdges = cv2.blur(edges,(2,2)) #averaging
    
                # 4.Hough line detection
                #frame = filters.applyHoughLinesP(edges,frame)
                
               #add final image to display
                self._captureManager.frame = blurredEdges
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