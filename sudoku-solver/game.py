from pprint import pprint

def find_next_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == -1:
                return r, c
    return None,None

# function to check if the guess is valid, it returns True if is_valid, otherwise False
def is_valid(board, guess, row, col):
    # check the row
    row_vals = board[row]
    if guess in row_vals:
        return False

    # check the cols
    # col_val = []
    # # for i in range(9):
    # #     col_val.append(board[i][col])
    col_vals = [board[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    # check the 3x3 grid
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if board[r][c] == guess:
                return False
    
    # approaching here these cheks pass
    return True
    

def solve_sudoku(board):
    # choose a place on the board to make a guess
    row, col = find_next_empty(board)

    # if there's no place left, then we're done because we only allowed valid inputs
    if row is None:
        return True

    # make a guess between 1 and 9
    for guess in range(1, 10):
        # check if this is a valid guess
        if is_valid(board, guess, row, col):
            # if valid, place the guess on the board
            board[row][col] = guess
            # recursively call solve_sudoku
            if solve_sudoku(board):
                return True
            # if not valid, reset the guess and try again
            board[row][col] = -1
    # if no valid guess is found, then this puzzle isn unsolvable and return False
    return False

if __name__ == '__main__':
    example_board = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]
    
    print(solve_sudoku(example_board))
    pprint(example_board)