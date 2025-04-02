import numpy as np

def create_board():
    cols = 7
    rows = 6
    board = np.zeros((rows,cols))
    return board

print(create_board())
