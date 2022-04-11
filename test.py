import cv2
import time
import filters
import houghTransform
import guitar



# define a video capture object
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    gaussianFiltered = filters.applyGaussianBlur(frame)
    edges = filters.autoCannyEdge(gaussianFiltered)
    
    """Get the string lines"""
    lines = houghTransform.getHoughLinesP(edges)
        # Draw the lines
    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            dx = (l[2]-l[0])
            if dx == 0:
                break
            gradient = (l[3] - l[1])/dx
            if gradient > 1:
                cv2.line(frame, (l[0], l[1]), (l[2], l[3]), (0,255,255), 2, cv2.LINE_AA)
  
  
    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
