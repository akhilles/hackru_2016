import cv2
import copy
import numpy as np


while(True):
    img =  cv2.imread('chessboard.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    thresh = cv2.GaussianBlur(thresh,(5,5),0)
    threshC = copy.deepcopy(thresh)
    _, contours, _= cv2.findContours(threshC, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest = None
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 10:
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.02*peri,True)
                if area > max_area and len(approx)==4:
                        biggest = approx
                        max_area = area
                        
    cv2.drawContours(threshC, biggest,-1, (255,0,0), 3)
    cv2.imshow('frame',thresh)
    cv2.imshow('frame2',gray)
    cv2.imshow('Contours',threshC)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
