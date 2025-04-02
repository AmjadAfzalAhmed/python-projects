import pygame
from network import Network
import pickle
pygame.font.init()

# dimensions of the game window
width = 700
height = 700

# creates the game window
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# creates the button class
class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    # draws the button
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        # centers the text
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    # checks if the button is clicked
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        # checks if the mouse is over the button
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

# redraws the window
def redrawWindow(win, game, p):
    win.fill((128,128,128)) # fills the window with a color

    if not(game.connected()): # if the game is not connected
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        # centers the text to the screen
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else: # if the game is connected
        font = pygame.font.SysFont("comicsans", 60) # font size
        text = font.render("Your Move", 1, (0, 255,255)) # text
        win.blit(text, (80, 200)) # position on screen

        text = font.render("Opponents", 1, (0, 255, 255)) # text
        win.blit(text, (380, 200)) # position

        move1 = game.get_player_move(0) # player 1 move
        move2 = game.get_player_move(1) # player 2 move
        if game.bothWent(): # if both players have played
            text1 = font.render(move1, 1, (0,0,0)) # player 1 move
            text2 = font.render(move2, 1, (0, 0, 0)) # player 2 move
        else: # if both players have not played
            if game.p1Went and p == 0: # if player 1 has played
                text1 = font.render(move1, 1, (0,0,0)) # player 1 move
            elif game.p1Went: # if player 1 has not played
                text1 = font.render("Locked In", 1, (0, 0, 0)) # player 1 move
            else: # if player 1 has not played
                text1 = font.render("Waiting...", 1, (0, 0, 0)) # player 1 move

            if game.p2Went and p == 1: # if player 2 has played
                text2 = font.render(move2, 1, (0,0,0)) # player 2 move
            elif game.p2Went: # if player 2 has not played
                text2 = font.render("Locked In", 1, (0, 0, 0)) # player 2 move
            else: # if player 2 has not played
                text2 = font.render("Waiting...", 1, (0, 0, 0)) # player 2 move

        if p == 1: # if player 2
            win.blit(text2, (100, 350)) # player 2 move
            win.blit(text1, (400, 350)) # player 1 move
        else: # if player 1
            win.blit(text1, (100, 350)) # player 1 move
            win.blit(text2, (400, 350)) # player 2 move

        for btn in btns: # for each button
            btn.draw(win) # draws the button

    pygame.display.update() # updates the display

# creates the buttons
btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]
def main(): # main function
    run = True # runs the game
    clock = pygame.time.Clock() # clock to control the frame rate
    n = Network() # network object
    player = int(n.getP()) # player
    print("You are player", player)

    while run: # while the game is running
        clock.tick(60) # controls the frame rate
        try:
            game = n.send("get") # gets the game
        except:
            run = False # stops the game
            print("Couldn't get game") # prints the error
            break # breaks the loop

        if game.bothWent(): # if both players have played
            redrawWindow(win, game, player) # redraws the window
            pygame.time.delay(500) # waits for 500ms
            try:
                game = n.send("reset") # resets the game
            except: # if there is an error
                run = False # stops the game
                print("Couldn't get game") # prints the error
                break # breaks the loop

        if game.bothWent(): # if both players have played
            redrawWindow(win, game, player) # redraws the window
            pygame.time.delay(500) # waits for 500ms
            try:
                game = n.send("reset") # resets the game
            except:
                run = False # stops the game
                print("Couldn't get game") # prints the error
                break # breaks the loop

            font = pygame.font.SysFont("comicsans", 90) # font size
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0): # if player 1 wins
                text = font.render("You Won!", 1, (255,0,0)) # text
            elif game.winner() == -1: # if it's a tie 
                text = font.render("Tie Game!", 1, (255,0,0)) # text
            else: # if player 2 wins
                text = font.render("You Lost...", 1, (255, 0, 0)) # text

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2)) # centers the text
            pygame.display.update() # updates the display
            pygame.time.delay(2000) # waits for 2000ms

        for event in pygame.event.get(): # for each event
            if event.type == pygame.QUIT: # if the event is quit
                run = False # stops the game 
                pygame.quit() # quits pygame

            if event.type == pygame.MOUSEBUTTONDOWN: # if the event is mouse button down
                pos = pygame.mouse.get_pos() # gets the position of the mouse 
                for btn in btns: # for each button
                    if btn.click(pos) and game.connected(): # if the button is clicked and the game is connected
                        if player == 0: # if player 1
                            if not game.p1Went: # if player 1 has not played
                                n.send(btn.text) # sends the button text
                        else: # if player 2
                            if not game.p2Went: # if player 2 has not played
                                n.send(btn.text) # sends the button text
        # redraws the window
        redrawWindow(win, game, player)

def menu_screen(): # menu screen
    run = True # runs the menu
    clock = pygame.time.Clock() # clock to control the frame rate

    while run: # while the menu is running
        clock.tick(60) # controls the frame rate
        win.fill((128, 128, 128)) # fills the window with a color
        font = pygame.font.SysFont("comicsans", 60) # font size
        text = font.render("Click to Play!", 1, (255,0,0)) # text
        win.blit(text, (100,200)) # position of the text on the screen
        pygame.display.update() # updates the display

        for event in pygame.event.get(): # for each event
            if event.type == pygame.QUIT: # if the event is quit
                pygame.quit() # quits pygame
                run = False # stops the menu
            if event.type == pygame.MOUSEBUTTONDOWN: # if the event is mouse button down
                run = False # stops the menu

    main() # starts the game

while True: # while the game is running
    menu_screen() # starts the menu
