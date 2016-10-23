import cv2
import time 
import copy
import numpy as np
global default_matrix
numFramesStill = 0

moveList = []
prevOccupancy = None
prevFrame = None
warped = False
retval = None
gameStarted = False

def get_differences(matrix_old, matrix_new):
    differences = []
    for rank in range(0,8):
        for filee in range(0,8):
            if (matrix_old[rank][filee] != matrix_new[rank][filee]):
                differences.append((rank, filee))
    return differences

def to_fen_notation(move):
    f_old = chr(ord('a') + move[0][1])
    r_old = str(move[0][0] + 1)
    f_new = chr(ord('a') + move[1][1])
    r_new = str(move[1][0] + 1)
    return f_old + r_old + f_new + r_new

def get_move(matrix_old, matrix_new):
    differences = get_differences(matrix_old, matrix_new)
    length = len(differences)
    if (length == 2):
        if (matrix_new[differences[0][0]][differences[0][1]] != 0):
            return to_fen_notation((differences[1],differences[0]))
        else:
            return to_fen_notation((differences[0],differences[1]))
    elif (length == 3):
        start = None
        end = None
        for difference in differences:
            if (matrix_new[difference[0]][difference[1]] != 0): end = difference
        for difference in differences:
            if (end[0] != difference[0] and end[1] != difference[1]): start = difference
        return to_fen_notation((start,end))
    elif (length == 4):
        if ((0,7) in differences): return 'e1g1'
        elif ((0,0) in differences): return 'e1c1'
        elif ((7,7) in differences): return 'e8g8'
        elif ((7,0) in differences): return 'e8c8'
        else: return '???'
    return '???'

def send_move_list(move_list):
    print 'sending move list to server'
    params = [('moves',str(move_list).replace("'", '"').replace(" ",""))]
    url = 'http://172.27.165.50:3000/'
    r = requests.get(url, params)
    print 'recieved suggested move: ' + r.text

def getBoardOccupancy(pValues):
        w = 8
        h = 8
        mat = [[0 for x in range(w)] for y in range(h)]
        for x in range(0,8):
                for y in range(0,8):
                        #difference_sum = 0
                        difference_sum = abs(pValues[x][y][2] - default_matrix[x][y][2])
                        print(difference_sum)
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
                        for i in range(5,34):
                                for j in range(5,34):
                                        tot = tot+ img[40*x+i,40*y+j]
                        mat[x][y] = (tot[0]/(30*30),tot[1]/(30*30),tot[2]/(30*30))
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
                        #sBiggest = biggest
                        biggest = approx
                        max_area = area
    return biggest


cap = cv2.VideoCapture("http://172.27.99.231:8080/video")
while(True):
    #img =  cv2.imread('chessboard2.jpg')
    #time.sleep(.1)
    ret, img =  cap.read()

    if ret==True and warped==False:
        img = cv2.GaussianBlur(img,(5,5),0)
        cv2.imshow('frame',img)

    if ret==True and warped==True:
        warp = cv2.warpPerspective(img,retval,(320,320))
        cv2.imshow('frame',warp)
        mat1 = pValues(warp)
        if(prevFrame != None):
                if(noChange(mat1) <500):
                        numFramesStill = numFramesStill+1
                else:
                        numFramesStill = 0
        prevFrame =mat1
        if(numFramesStill > 20):
                occupancy = getBoardOccupancy(mat1)
                if (prevOccupancy != None and prevOccupancy != occupancy):
                        print_board(occupancy)
                        if (gameStarted):
                                move = get_move(prevOccupancy)
                                print move
                if (gameStarted == False and occupancy == initial_board()):
                        gameStarted = True
                numFramesStill = 0
                prevOccupancy = occupancy

    
    if cv2.waitKey(1) & 0xFF == ord('f'):
        if ret==True:
            print 'finding corners'
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray,(5,5),0)
            thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
            _, contours, _= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            biggest = biggestContour(contours)
            approx = rectify(biggest)
            h = np.array([ [0,0],[319,0],[319,319],[0,319] ],np.float32)
            retval = cv2.getPerspectiveTransform(approx,h)
            warp = cv2.warpPerspective(img,retval,(320,320))
            cv2.imshow('warp',warp)
            warped = True
            default_matrix = pValues(warp)
            

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
