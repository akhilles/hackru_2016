import cv2
import copy
import numpy as np
global default_matrix
numFramesStill = 0

prevFrame = None
warped = False
retval = None
gameStarted = False

def getBoardOccupancy(pValues):
        w = 8
        h = 8
        mat = [[0 for x in range(w)] for y in range(h)]
        for x in range(0,8):
                for y in range(0,8):
                        #difference_sum = 0
                        difference_sum = abs(pValues[x][y][2] - default_matrix[x][y][2])
                        #for i in range(0,3):
                                #difference_sum = difference_sum + pValues[x][y][i] - default_matrix[x][y][i]
                        if (difference_sum < 8):
                                mat[x][y] = 0
                        else:
                                mat[x][y] = 1
        return mat

def noChange(newFrame):
        sum1 = 0
        for x in range(0,8):
                for y in range(0,8):
                        for i in range(0,3):
                                sum1 = sum1+abs(newFrame[x][y][i]-prevFrame[x][y][i])
        #print sum1
        return sum1


def print_board(matrix):
    for rank in (matrix):
        print rank
    print
    
def pValues(img):
        w = 8
        h = 8
        mat = [[0 for x in range(w)] for y in range(h)]
        for x in range(0,8):
                
                for y in range(0,8):
                        tot = [0,0,0]
                        for i in range(15,64):
                                for j in range(15,64):
                                        tot = tot+ img[80*x+i,80*y+j]
                        mat[x][y] = (tot[0]/(50*50),tot[1]/(50*50),tot[2]/(50*50))
        #print_board(mat)
        return mat

def initial_board():
    w = 8
    h = 8
    matrix = [[0 for x in range(w)] for y in range(h)]
    for f in range(0,8):
        for r in range(0,2):
            matrix[r][f] = 1
        for r_b in range(6,8):
            matrix[r_bq][f] = 1
    return matrix

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


cap = cv2.VideoCapture("http://172.27.228.21:8080/video")
while(True):
    #img =  cv2.imread('chessboard2.jpg')
    ret, img =  cap.read()

    if ret==True and warped==False:
        img = cv2.GaussianBlur(img,(5,5),0)
        cv2.imshow('frame',img)

    if ret==True and warped==True:
        warp = cv2.warpPerspective(img,retval,(640,640))
        cv2.imshow('frame',warp)
        mat1 = pValues(warp)
        if(prevFrame != None):
                if(noChange(mat1) <500):
                        occupancy = getBoardOccupancy(mat1)
                        print_board(occupancy)
                        numFramesStill = numFramesStill+1
                else:
                        numFramesStill = 0
        prevFrame =mat1
        
        #if (numFramesStill >= 10):
                #if (gameStarted == False):

                
    
    if cv2.waitKey(1) & 0xFF == ord('f'):
        if ret==True:
            print 'finding corners'
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray,(5,5),0)
            thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
            _, contours, _= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            biggest = biggestContour(contours)
            approx = rectify(biggest)
            h = np.array([ [0,0],[639,0],[639,639],[0,639] ],np.float32)
            retval = cv2.getPerspectiveTransform(approx,h)
            warp = cv2.warpPerspective(img,retval,(640,640))
            cv2.imshow('warp',warp)
            warped = True
            default_matrix = pValues(warp)
            

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
