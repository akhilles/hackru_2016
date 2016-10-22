import cv2
import copy
import numpy as np
#from skimage import io, img_as_float

def pValues(img):
        w = 8
        h = 8
        mat = [[0 for x in range(w)] for y in range(h)]
        for x in range(0,7):
                print "\n"
                for y in range(0,7):
                        img1 = img[80*x:80*(x+1),80*y:80*(y+1)]
                        #img1 = img_as_float(img1)
                        mat[x,y] = img1.mean()
                        print mat[x,y]
        return mat


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

def biggestContour(c):
    biggest = None
    max_area = 0
    for i in c:
        area = cv2.contourArea(i)
        if area > 10:
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.02*peri,True)
                if area > max_area and len(approx)==4:
                        #approx = rectify(approx)
                        sBiggest = biggest
                        biggest = approx
                        max_area = area
    return biggest


#cap = cv2.VideoCapture("http://172.27.228.21:8080/video")
while(True):
    img =  cv2.imread('chessboard7.jpg')
    #ret, img =  cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    #thresh = cv2.GaussianBlur(thresh,(5,5),0)
    threshC = copy.deepcopy(thresh)
    _, contours, _= cv2.findContours(threshC, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

                        
    biggest = biggestContour(contours)
    cv2.drawContours(threshC, biggest,-1, (255,0,0), 3)
    cv2.imshow('frame',thresh)
    cv2.imshow('frame2',gray)
    cv2.imshow('Contours',threshC)
    approx = rectify(biggest)
    h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)
    retval = cv2.getPerspectiveTransform(approx,h)
    warp = cv2.warpPerspective(gray,retval,(450,450))
    cv2.imshow('warp',warp)


    threshW =  cv2.adaptiveThreshold(warp,255,1,1,11,2)
    #threshW = cv2.GaussianBlur(threshW,(5,5),0)
    
    _, contoursW, _= cv2.findContours(threshW, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    biggestW = biggestContour(contoursW)
    cv2.drawContours(threshW, biggestW,-1, (255,0,0), 3)
    cv2.imshow('warp2',threshW)
    approxW = rectify(biggestW)
    retval = cv2.getPerspectiveTransform(approxW,h)
    warp2 = cv2.warpPerspective(warp,retval,(450,450))
    cv2.imshow('warp2',warp2)
    pValues(warp2)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
