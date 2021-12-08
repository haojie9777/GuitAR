import cv2
import numpy as np

def removeDuplicateLines(lines):
    if lines is None:
        return
    strong_lines = np.zeros([10,1,2])
        
    n2 = 0
    for n1 in range(0,len(lines)):
        for rho,theta in lines[n1]:
            if n1 == 0:
                strong_lines[n2] = lines[n1]
                n2 = n2 + 1
            else:
                if rho < 0:
                    rho*=-1
                    theta-=np.pi
                closeness_rho = np.isclose(rho,strong_lines[0:n2,0,0],atol = 10)
                closeness_theta = np.isclose(theta,strong_lines[0:n2,0,1],atol = np.pi/36)
                closeness = np.all([closeness_rho,closeness_theta],axis=0)
                if not any(closeness) and n2 < 10:
                        strong_lines[n2] = lines[n1]
                        n2 = n2 + 1
    return strong_lines


def drawVerticalLines(lines, frame):
    if lines is None:
        return
    
            
    
    import cv2
import numpy as np

def removeDuplicateLines(lines):
    if lines is None:
        return
    strong_lines = np.zeros([10,1,2])
        
    n2 = 0
    for n1 in range(0,len(lines)):
        for rho,theta in lines[n1]:
            if n1 == 0:
                strong_lines[n2] = lines[n1]
                n2 = n2 + 1
            else:
                if rho < 0:
                    rho*=-1
                    theta-=np.pi
                closeness_rho = np.isclose(rho,strong_lines[0:n2,0,0],atol = 10)
                closeness_theta = np.isclose(theta,strong_lines[0:n2,0,1],atol = np.pi/36)
                closeness = np.all([closeness_rho,closeness_theta],axis=0)
                if not any(closeness) and n2 < 10:
                        strong_lines[n2] = lines[n1]
                        n2 = n2 + 1
    return strong_lines


def drawVerticalLines(lines, frame):
    if lines is None:
        return
    
            
    
    