state = -1

class State:
    initial, corners_detected, tracking_state = range(3)

class Pieces:
    empty, white, black = range(3)

w = 8
h = 8
Matrix = [[0 for x in range(w)] for y in range(h)]

def initialize(matrix):
    matrix[0][0] = Pieces.WHITE
    return matrix

def print_board(matrix):
    for rank in reversed(matrix):
        print rank

for f in range(0,8):
    for r in range(0,2):
        Matrix[r][f] = Pieces.white
    for r_b in range(6,8):
        Matrix[r_b][f] = Pieces.black

print_board(Matrix)