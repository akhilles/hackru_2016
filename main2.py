state = -1

class State:
    initial, corners_detected, tracking_state = range(3)

class Pieces:
    empty, white, black = range(3)

w = 8
h = 8

def initialize(matrix):
    for f in range(0,8):
        for r in range(0,2):
            matrix[r][f] = Pieces.white
        for r_b in range(6,8):
            matrix[r_b][f] = Pieces.black
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

def compare(matrix_old, matrix_new):
    differences = get_differences(matrix_old, matrix_new)
    length = len(differences)
    if (length == 2):
        if (matrix_new[differences[0][0]][differences[0][1]] != 0):
            return(differences[1],differences[0])
        else:
            return(differences[0],differences[1])
    return 0

Matrix1 = [[0 for x in range(w)] for y in range(h)]
Matrix2 = [[0 for x in range(w)] for y in range(h)]

Matrix1 = initialize(Matrix1)
Matrix2 = initialize(Matrix2)

Matrix2[3][3] = Pieces.white
Matrix2[1][3] = Pieces.empty

print_board(Matrix1)
print_board(Matrix2)
print get_differences(Matrix1, Matrix2)
print compare(Matrix1, Matrix2)