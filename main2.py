import requests

state = -1

class State:
    initial, corners_detected, tracking_state = range(3)

def initial_board():
    w = 8
    h = 8
    matrix = [[0 for x in range(w)] for y in range(h)]
    for f in range(0,8):
        for r in range(0,2):
            matrix[r][f] = 1
        for r_b in range(6,8):
            matrix[r_b][f] = 1
    return matrix

def print_board(matrix):
    for rank in reversed(matrix):
        print rank
    print

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

Matrix1 = initial_board()
Matrix2 = initial_board()

Matrix2[1][5] = 0
Matrix2[3][5] = 1

print_board(Matrix1)
print_board(Matrix2)
print get_differences(Matrix1, Matrix2)
move = get_move(Matrix1, Matrix2)
print move

move_list = []
move_list.append(move)

send_move_list(move_list)