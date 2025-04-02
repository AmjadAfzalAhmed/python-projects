import math # Import math module for mathematical operations
import random # Import random module for generating random numbers
import pygame # Import pygame module for game development
from pygame import mixer # Import mixer module from pygame for sound handling


# Initialize pygame
pygame.init()

# Set up the game window with size 800x600
screen = pygame.display.set_mode((800, 600))

# Load background image for the game
background = pygame.image.load('background.png')

# Game Sound: Load and play background music in a loop
mixer.music.load("background.wav")
mixer.music.play(-1)

# Set game window caption and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player setup: image, initial position, and movement speed
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 5

# Enemy setup: Initialize empty lists to hold enemy images, positions, and movement data
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6  # Set number of enemies

# Initialize enemies' images and positions
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))  # Load enemy image
    enemyX.append(random.randint(0, 736))  # Random horizontal position
    enemyY.append(random.randint(50, 150))  # Random vertical position
    enemyX_change.append(4)  # Speed of horizontal movement
    enemyY_change.append(40)  # Speed of vertical movement

# Bullet setup:
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 25
bullet_state = "ready"  # "ready" means bullet is not on screen, "fire" means bullet is moving

# Score setup: Initialize score and font for rendering text
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Position for displaying score
textX = 10
testY = 10

# Game Over font setup
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Function to display the current score
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))  # Render score text
    screen.blit(score, (x, y))  # Blit (draw) the score on the screen at specified position

# Function to display game over text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))  # Render "GAME OVER" text
    screen.blit(over_text, (200, 250))  # Blit (draw) the "GAME OVER" text on the screen

# Function to display the player spaceship
def player(x, y):
    screen.blit(playerImg, (x, y))  # Draw the player's spaceship at (x, y) coordinates

# Function to display the enemies on the screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # Draw the i-th enemy at (x, y) coordinates

# Function to handle bullet firing
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"  # Change bullet state to "fire" to indicate it's moving
    screen.blit(bulletImg, (x + 16, y + 10))  # Draw the bullet at the player’s position

# Function to detect collisions between bullet and enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))  # Calculate distance between enemy and bullet
    if distance < 27:  # If distance is less than a certain threshold, collision is detected
        return True
    else:
        return False

# Main Game Loop
running = True
while running:
    # Fill the screen with black color (RGB = 0, 0, 0)
    screen.fill((0, 0, 0))
    
    # Draw the background image
    screen.blit(background, (0, 0))

    # Event handling (keyboard and quit events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Close the game window if the quit button is clicked

        # Check if a key is pressed down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Move player left
                playerX_change = -5
            if event.key == pygame.K_RIGHT:  # Move player right
                playerX_change = 5
            if event.key == pygame.K_SPACE:  # Fire the bullet when space key is pressed
                if bullet_state == "ready":  # Only fire if bullet is ready
                    bulletSound = mixer.Sound("laser.wav")  # Load and play laser sound
                    bulletSound.play()
                    bulletX = playerX  # Set bullet's initial X position to player's X position
                    fire_bullet(bulletX, bulletY)  # Fire the bullet
            if event.key == pygame.K_ESCAPE:  # Escape key to exit the game
                running = False

        # Reset player's horizontal movement when key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement logic: Ensure the player doesn't move out of bounds
    playerX += playerX_change
    if playerX <= 0:  # Prevent player from going off the left side of the screen
        playerX = 0
    elif playerX >= 736:  # Prevent player from going off the right side of the screen
        playerX = 736

    # Enemy movement logic: Handle the horizontal movement and bouncing of enemies
    for i in range(num_of_enemies):
        # Game Over: If an enemy reaches the player’s Y position, game ends
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # Move enemies off-screen
            game_over_text()  # Display "Game Over" text
            break

        # Move enemies horizontally and change direction if they hit the screen boundaries
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:  # If enemy reaches the left boundary, move right
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]  # Move the enemy down slightly
        elif enemyX[i] >= 736:  # If enemy reaches the right boundary, move left
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]  # Move the enemy down slightly

        # Check for collision between bullet and enemy
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")  # Play explosion sound on collision
            explosionSound.play()
            bulletY = 480  # Reset bullet's Y position
            bullet_state = "ready"  # Set bullet state back to "ready"
            score_value += 1  # Increase score by 1
            enemyX[i] = random.randint(0, 736)  # Reset enemy’s position after destruction
            enemyY[i] = random.randint(50, 150)  # Reset enemy’s Y position

        # Display each enemy on the screen
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement: Reset bullet if it goes off-screen
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # If the bullet is fired, move it upwards
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Display player and score
    player(playerX, playerY)
    show_score(textX, testY)

    # Update the display
    pygame.display.update()
