import cv2
import copy
import numpy as np

def rectify(h):
        h = h.reshape((4,2))
        hnew = np.zeros((4,2),dtype = np.float32)
 
        add = h.sum(1)
        hnew[0] = h[np.argmin(add)]
        hnew[2] = h[np.argmax(add)]
         
        diff = np.diff(h,axis = 1)
        hnew[1] = h[np.argmin(diff)]
        hnew[3] = h[np.argmax(diff)]
  
        return hnew


while(True):
    img =  cv2.imread('chessboard2.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    #thresh = cv2.GaussianBlur(thresh,(5,5),0)
    threshC = copy.deepcopy(thresh)
    _, contours, _= cv2.findContours(threshC, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest = None
    max_area = 0
    index = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 10:
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.02*peri,True)
                if area > max_area and len(approx)==4:
                        #approx = rectify(approx)
                        biggest = approx
                        max_area = area
                        index = i
                        
    cv2.drawContours(threshC, biggest,-1, (255,0,0), 3)
    cv2.imshow('frame',thresh)
    cv2.imshow('frame2',gray)
    cv2.imshow('Contours',threshC)
    approx = rectify(biggest)
    h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)
    retval = cv2.getPerspectiveTransform(approx,h)
    warp = cv2.warpPerspective(gray,retval,(450,450))
    cv2.imshow('warp',warp)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
