import pygame
import random

# Global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
play_width = 300
play_height = 600
BLOCK_SIZE = 30

# top left of the play area
top_left_x = (SCREEN_WIDTH - play_width) // 2
top_left_y = SCREEN_HEIGHT - play_height 

# Shape Formats
S = [['.....',
        '.....',
        '..00.',
        '.00..',
        '.....'],
       ['.....',
        '..0..',
        '..00.',
        '...0.',
        '.....']]

Z = [['.....',
        '.....',
        '.00..',
        '..00.',
        '.....'],
       ['.....',
        '..0..',
        '.00..',
        '.0...',
        '.....']]

I =  [['.....',
        '..0..',
        '..0..',
        '..0..',
        '..0..'],
      ['.....',
        '00000',
        '.....',
        '.....',
        '.....']]

O =  [['.....',
        '.....',
        '.00..',
        '.00..',
        '.....']]

J =  [['.....',
        '.0...',
        '.000.',
        '.....',
        '.....'],
       ['.....',
        '..00.',
        '..0..',
        '..0..',
        '.....'],
         ['.....',
        '.....',
        '.000.',
        '...0.',
        '.....'],
         ['.....',
        '..0..',
        '..0..',
        '.00..',
        '.....']]

L =  [['.....',
        '...0.',
        '.000.',
        '.....',
        '.....'],
       ['.....',
        '..0..',
        '..0..',
        '..00.',
        '.....'],
         ['.....',
        '.....',
        '.000.',
        '.0...',
        '.....'],
         ['.....',
        '.00..',
        '..0..',
        '..0..',
        '.....']]

T = [['.....',
        '..0..',
        '.000.',
        '.....',
        '.....'],
       ['.....',
        '..0..',
        '..00.',
        '..0..',
        '.....'],
         ['.....',
        '.....',
        '.000.',
        '..0..',
        '.....'],
         ['.....',
        '..0..',
        '.00..',
        '..0..',
        '.....']]

# List of shapes
# Each shape is represented by a list of strings, where '0' represents a block and '.' represents empty space
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# Piece class
# Each piece is represented by a list of strings, where '0' represents a block and '.' represents empty space
class Piece(object):
    def __init__(self,x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
        self.shape_format = convert_shape_format(self)

# Create a grid
# Each cell in the grid is a tuple of RGB values
# (0,0,0) represents an empty cell
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    # loop through the locked positions and add them to the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

# Convert shape to positions
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    # loop through the format and add the positions to the list
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j -2 , shape.y + i - 4))
    # adjust the positions
    for i , pos in enumerate(positions):
        positions[i] = (pos[0] -2, pos[1] - 4)

    return positions

# Check if the shape is in a valid space
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    
    # convert the shape to positions
    formatted = convert_shape_format(shape)
    # check if the shape is in a valid space
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] >= 0:
                return False
    return True

# Check if the game is lost
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

# Function to draw the grid lines on the screen
def get_shape():
    return Piece(5,0, random.choice(shapes))

# Function to draw text in the middle of the screen
def draw_text_middle(surface,text, size, color):
    # Initialize the font
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    # Draw the text in the middle of the screen
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))

# Function to draw the grid lines on the screen
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    # Draw the grid lines
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * BLOCK_SIZE), (sx + play_width, sy + i * BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * BLOCK_SIZE, sy), (sx + j * BLOCK_SIZE, sy + play_height))

# Function to clear rows
# This function removes completed rows from the grid and updates the locked positions
def clear_rows(grid, locked):
    increment = 0
    # Loop through the grid and remove completed rows
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            increment += 1
            index = i
            # Remove the completed row from the grid
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    # Update the locked positions
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < index:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
        
    return increment

# This function draws the next shape on the screen
def draw_next_shape(shape, surface):
    # Initialize the font
    pygame.font.init()
    
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
    # Draw the next shape
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                # Draw the shape
                pygame.draw.rect(surface, shape.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    # Draw the label
    surface.blit(label, (sx + 10, sy - 30))

# This function updates the score in the file    
def update_score(nscore):
    score = max_score()
    # Update the score
    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

# This function returns the maximum score
def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    
    return score

# This function draws the window and updates the display
def draw_window(surface,grid,score=0, last_score=0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    # Draw the label
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    # Draw the current score
    surface.blit(label, (sx + 20, sy + 160))
    
    # last score
    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))
    sx = top_left_x - 240
    sy = top_left_y + 200
    # Draw the last score
    surface.blit(label, (sx + 20, sy + 160))

    # Draw the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # Draw the grid
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * BLOCK_SIZE, top_left_y + i * BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE), 0)
    # Draw the border
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5) #this is the border of the play area

    draw_grid(surface, grid)
    # pygame.display.update()

# This function is the main function    
def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    # Main loop
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # Level up
        if level_time / 1000 >= 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        # Fall speed
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            
            # Key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
        
        # Convert the shape to positions
        shape_pos = convert_shape_format(current_piece)
        # Draw the shape
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y >= -1:
                grid[y][x] = current_piece.color
        # Update the locked positions
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color

            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
            print(score)                
        # Draw the window
        draw_window(win,grid,score,last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        clear_rows(grid, locked_positions)
        # Check if the player lost
        if check_lost(locked_positions):
            draw_text_middle(win, 'YOU LOST', 80, (255, 0, 0))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False 
            update_score(score)

# This function is the main menu function
def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Press any key to play', 60, (255, 255, 255))
        pygame.display.update()
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    # Quit pygame
    pygame.display.quit()
# Initialize pygame
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
# Run the main menu
main_menu(win)