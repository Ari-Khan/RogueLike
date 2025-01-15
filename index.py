#########################################
# File Name: index.py
# Description: Rogue-Like Game where players use a shooting mechanism to fight off hordes of zombies.
# Author: Ari Khan
# Date: 01/09/2025
#########################################

import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2

# Field dimensions
FIELD_SIZE = 1000

# Colors
WHITE = (255, 255, 255)
LIGHT_GREEN = (60, 255, 80)
DARK_GREEN = (0, 100, 0)
BLUE = (50, 100, 250)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

PLAYER_RADIUS = 30
BULLET_RADIUS = 5
BULLET_SPEED = 10
ZOMBIE_RADIUS = 25
ZOMBIE_SPEED = 2

FONT_SIZE = 25
FPS = 60

# Setup display
gameWindow = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Shooter Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Movement speed
speed = 5

# Bullet data
bulletX = []
bulletY = []
bulletDirection = []

# Zombie data
zombieX = []
zombieY = []
zombieHealth = []

# Game variables
score = 0
highScore = 0
font = pygame.font.SysFont("OCR-A Extended", FONT_SIZE)

# Spawn zombies in the corners of the map
def spawn_zombie(fieldX, fieldY):
    corners = [(fieldX, fieldY), (fieldX + FIELD_SIZE, fieldY), (fieldX, fieldY + FIELD_SIZE), (fieldX + FIELD_SIZE, fieldY + FIELD_SIZE)]
    x, y = random.choice(corners)
    zombieX.append(x)
    zombieY.append(y)
    zombieHealth.append(5)

# Shift functions
def shift_up(amount, fieldY, bulletY, zombieY):
    fieldY += amount
    bulletY = [y + amount for y in bulletY]
    zombieY = [y + amount for y in zombieY]
    return fieldY, bulletY, zombieY

def shift_down(amount, fieldY, bulletY, zombieY):
    fieldY -= amount
    bulletY = [y - amount for y in bulletY]
    zombieY = [y - amount for y in zombieY]
    return fieldY, bulletY, zombieY

def shift_left(amount, fieldX, bulletX, zombieX):
    fieldX += amount
    bulletX = [x + amount for x in bulletX]
    zombieX = [x + amount for x in zombieX]
    return fieldX, bulletX, zombieX

def shift_right(amount, fieldX, bulletX, zombieX):
    fieldX -= amount
    bulletX = [x - amount for x in bulletX]
    zombieX = [x - amount for x in zombieX]
    return fieldX, bulletX, zombieX

# Game drawing function
def draw_game(gameWindow, fieldX, fieldY, score, highScore):
    # Clear the screen with a dark green background
    gameWindow.fill(DARK_GREEN)

    # Draw the square background (1000x1000 field)
    pygame.draw.rect(gameWindow, LIGHT_GREEN, (fieldX, fieldY, FIELD_SIZE, FIELD_SIZE))

    # Draw bullets
    for i in range(len(bulletX)):
        pygame.draw.circle(gameWindow, BLUE, (int(bulletX[i]), int(bulletY[i])), BULLET_RADIUS)

    # Draw zombies
    for i in range(len(zombieX)):
        pygame.draw.circle(gameWindow, RED, (int(zombieX[i]), int(zombieY[i])), ZOMBIE_RADIUS)

    # Draw the player as a circle centered on the screen
    pygame.draw.circle(gameWindow, BLUE, (CENTER_X, CENTER_Y), PLAYER_RADIUS)

    # Draw score and high score
    scoreText = font.render(f"Score: {score}", True, WHITE)
    highScoreText = font.render(f"High Score: {highScore}", True, BLUE)
    gameWindow.blit(scoreText, (20, 20))
    gameWindow.blit(highScoreText, (SCREEN_WIDTH - 200, 20))

    pygame.display.update()

# Home screen
def home_screen():
    gameWindow.fill(LIGHT_GREEN)
    titleText = font.render("Zombie Shooter Game", True, BLUE)
    playText = font.render("Press SPACE to Start", True, BLUE)
    highScoreText = font.render(f"High Score: {highScore}", True, BLUE)

    gameWindow.blit(titleText, (CENTER_X - 150, CENTER_Y - 100))
    gameWindow.blit(playText, (CENTER_X - 140, CENTER_Y))
    gameWindow.blit(highScoreText, (CENTER_X - 110, CENTER_Y + 100))
    pygame.display.update()

# Main game loop
inPlay = True
spawn_timer = 0
bullet_timer = 0
fieldX = CENTER_X - FIELD_SIZE // 2
fieldY = CENTER_Y - FIELD_SIZE // 2

showHome = True
while inPlay:
    if showHome:
        home_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                score = 0
                showHome = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    if keys[pygame.K_a] and fieldX < CENTER_X - PLAYER_RADIUS:
        fieldX, bulletX, zombieX = shift_left(speed, fieldX, bulletX, zombieX)
    if keys[pygame.K_d] and fieldX > CENTER_X - FIELD_SIZE + PLAYER_RADIUS:
        fieldX, bulletX, zombieX = shift_right(speed, fieldX, bulletX, zombieX)
    if keys[pygame.K_w] and fieldY < CENTER_Y - PLAYER_RADIUS:
        fieldY, bulletY, zombieY = shift_up(speed, fieldY, bulletY, zombieY)
    if keys[pygame.K_s] and fieldY > CENTER_Y - FIELD_SIZE + PLAYER_RADIUS:
        fieldY, bulletY, zombieY = shift_down(speed, fieldY, bulletY, zombieY)

    # Shooting bullets (limit to 4 bullets per second)
    bullet_timer += clock.get_time()
    if mouse[0] and bullet_timer >= 200:
        bulletX.append(CENTER_X)
        bulletY.append(CENTER_Y)
        mouseX, mouseY = pygame.mouse.get_pos()
        angle = math.atan2(mouseY - CENTER_Y, mouseX - CENTER_X)
        bulletDirection.append((math.cos(angle), math.sin(angle)))
        bullet_timer = 0

    # Update bullets
    for i in range(len(bulletX)):
        bulletX[i] += bulletDirection[i][0] * BULLET_SPEED  # X component
        bulletY[i] += bulletDirection[i][1] * BULLET_SPEED  # Y component

    for i in range(len(zombieX) - 1, -1, -1):
        # Move zombies towards the player
        dx = CENTER_X - zombieX[i]
        dy = CENTER_Y - zombieY[i]
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            zombieX[i] += ZOMBIE_SPEED * dx / distance
            zombieY[i] += ZOMBIE_SPEED * dy / distance

        # Check for bullet collisions
        for e in range(len(bulletX) - 1, -1, -1):
            bullet_dx = bulletX[e] - zombieX[i]
            bullet_dy = bulletY[e] - zombieY[i]
            bullet_distance = math.sqrt(bullet_dx**2 + bullet_dy**2)

            if bullet_distance < BULLET_RADIUS + ZOMBIE_RADIUS:
                zombieHealth[i] -= 1
                del bulletX[e]
                del bulletY[e]
                del bulletDirection[e]

                if zombieHealth[i] <= 0:
                    del zombieX[i]
                    del zombieY[i]
                    del zombieHealth[i]
                    score += 1
                    if score > highScore:
                        highScore = score

    # Spawn zombies every 2 seconds
    spawn_timer += 1
    if spawn_timer >= FPS*2:
        spawn_zombie(fieldX, fieldY)
        spawn_timer = 0

    # Call the draw function
    draw_game(gameWindow, fieldX, fieldY, score, highScore)

    # Cap the frame rate to 60 FPS
    clock.tick(FPS)

pygame.quit()
