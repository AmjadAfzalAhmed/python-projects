import numpy as np
import pygame
import sys
import math

# Defining colors using RGB values 
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# Defining the dimensions of the game board
ROW_COUNT = 6
COLUMN_COUNT = 7

# Function to create an empty game board filled with zeros
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

# Function to drop a game piece into the board at the specified column
def drop_piece(board, row, col, piece):
	board[row][col] = piece # Places the piece (1 or 2) at the given row and column

# Function to check if a column has space for a new piece
def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0 # Checks if the topmost row of the column is empty

# Function to find the next available row in a column
def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r # Returns the first empty row found in the column

# Function to print the board with the latest moves
def print_board(board):
	print(np.flip(board, 0)) # Flips the board vertically for correct display

# Function to check if a player has won the game
def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3): # Iterate over all possible start positions
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertically for a win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3): # Check all possible vertical connections
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check diagonally (positive slope)
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):# Start from row index 3 to avoid out-of-bounds
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

# Function to draw the game board using Pygame
def draw_board(board):
	# loop to draw the board
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			# Draw the board slots (rectangles)
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			 # Draw empty circles in the slots
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	# Loop through the board to draw pieces
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1: # Player 1 (Red)
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: # Player 1 (Yellow) 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

# Initialize the game board
board = create_board()
print_board(board)
game_over = False
turn = 0 # 0 for Player 1, 1 for Player 2

# pygame initialization
pygame.init()

# square size
SQUARESIZE = 100

# width and height of the window
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

# radius of the pieces
RADIUS = int(SQUARESIZE/2 - 5)

# create the window
screen = pygame.display.set_mode(size)
# Draw the initial empty board
draw_board(board)
pygame.display.update()

# font for the game over message
myfont = pygame.font.SysFont("monospace", 75)

# game loop
while not game_over:

	# event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit() # Exit if window is closed

		# Handling player moves
		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		# mouse click
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))
				# check if the location is valid
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)
					# check for winning move
					if winning_move(board, 1):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True # Stop game if won

			# Ask for Player 2 Input
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))
				# check if the location is valid
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)
					# check for winning move
					if winning_move(board, 2):
						label = myfont.render("Player 2 wins!!", 1, YELLOW)
						screen.blit(label, (40,10))
						game_over = True
			
			
			print_board(board) # Print updated board in console
			draw_board(board) # Update graphics

			# switch turns
			turn += 1
			turn = turn % 2 
			# wait for 3 seconds
			if game_over:
				pygame.time.wait(3000)