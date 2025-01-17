#########################################
# File Name: main.py
# Description: Rogue-Like Game where players use a shooting mechanism to fight off hordes of zombies.
# Author: Ari Khan
# Date: 01/09/2025
#########################################

import pygame
import math
import random

# Initialize Pygame
pygame.init()

#---------------------------------------#
# Define Constants                      #
#---------------------------------------#

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

# Constants
PLAYER_RADIUS = 30
PLAYER_SPEED = 5
BULLET_RADIUS = 5
BULLET_SPEED = 10
ZOMBIE_RADIUS = 25
ZOMBIE_SPEED = 2
FONT_SIZE = 25
FPS = 60

#---------------------------------------#
# Initialize Objects/Variables          #
#---------------------------------------#

# Initialize music and sound effects
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.7)
chompSound = pygame.mixer.Sound("gunshot.wav")
chompSound.set_volume(1)

# Initialize game window
gameWindow = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock for frame rate
clock = pygame.time.Clock()

# Game variables
bulletX = []
bulletY = []
bulletDirection = []
zombieX = []
zombieY = []
zombieHealth = []
score = 0
highScore = 0
health = 3
last_hit_time = 0
spawn_interval = FPS * 2
font = pygame.font.SysFont("OCR-A Extended", FONT_SIZE)

# Spawn a zombie in a random corner
def spawn_zombie(fieldX, fieldY):
    corners = [
        (fieldX, fieldY),
        (fieldX + FIELD_SIZE, fieldY),
        (fieldX, fieldY + FIELD_SIZE),
        (fieldX + FIELD_SIZE, fieldY + FIELD_SIZE),
    ]
    x, y = random.choice(corners)
    zombieX.append(x)
    zombieY.append(y)
    zombieHealth.append(5)

# Shift functions for movement, moving game elements
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

# Draw game objects
def draw_game(gameWindow, fieldX, fieldY, score, highScore, health):
    gameWindow.fill(DARK_GREEN)
    pygame.draw.rect(gameWindow, LIGHT_GREEN, (fieldX, fieldY, FIELD_SIZE, FIELD_SIZE))

    for i in range(len(bulletX)):
        pygame.draw.circle(gameWindow, BLUE, (int(bulletX[i]), int(bulletY[i])), BULLET_RADIUS)
    for i in range(len(zombieX)):
        pygame.draw.circle(gameWindow, RED, (int(zombieX[i]), int(zombieY[i])), ZOMBIE_RADIUS)

    pygame.draw.circle(gameWindow, BLUE, (CENTER_X, CENTER_Y), PLAYER_RADIUS)

    scoreText = font.render(f"Score: {score}", True, WHITE)
    highScoreText = font.render(f"High Score: {highScore}", True, BLUE)
    healthText = font.render(f"Health: {health}", True, RED)
    gameWindow.blit(scoreText, (20, 20))
    gameWindow.blit(highScoreText, (SCREEN_WIDTH - 250, 20))
    gameWindow.blit(healthText, (20, 60))

    pygame.display.update()

# Show the home screen
def home_screen():
    gameWindow.fill(LIGHT_GREEN)

    titleText = font.render("Nuclear Survival", True, BLUE)
    playText = font.render("Press SPACE to Start", True, BLUE)
    highScoreText = font.render(f"High Score: {highScore}", True, BLUE)
    controlsText = font.render("Click to shoot and use WASD to move.", True, BLUE)
    goalText = font.render("Defeat red zombies to survive as long as possible.", True, BLUE)

    gameWindow.blit(titleText, (CENTER_X - 120, CENTER_Y - 150))
    gameWindow.blit(playText, (CENTER_X - 150, CENTER_Y - 100))
    gameWindow.blit(highScoreText, (CENTER_X - 110, CENTER_Y - 50))
    gameWindow.blit(controlsText, (CENTER_X - 275, CENTER_Y))
    gameWindow.blit(goalText, (CENTER_X - 375, CENTER_Y + 50))

    pygame.display.update()

# Show the game over screen
def game_over_screen(score, highScore):
    gameWindow.fill(LIGHT_GREEN)

    gameOverText = font.render("Game Over", True, BLUE)
    scoreText = font.render(f"Total Score: {score}", True, WHITE)
    highScoreText = font.render(f"High Score: {highScore}", True, BLUE)
    restartText = font.render("Press R to Restart", True, BLUE)
    homeText = font.render("Press H to Return to Home", True, BLUE)

    gameWindow.blit(gameOverText, (CENTER_X - 75, CENTER_Y - 150))
    gameWindow.blit(scoreText, (CENTER_X - 115, CENTER_Y - 100))
    gameWindow.blit(highScoreText, (CENTER_X - 110, CENTER_Y - 50))
    gameWindow.blit(restartText, (CENTER_X - 135, CENTER_Y))
    gameWindow.blit(homeText, (CENTER_X - 190, CENTER_Y + 50))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            return False
        if keys[pygame.K_h]:
            return True

# Main game loop
spawn_timer = 0
bullet_timer = 0
fieldX = CENTER_X - FIELD_SIZE // 2
fieldY = CENTER_Y - FIELD_SIZE // 2

pygame.mixer.music.play(loops=-1)
inPlay = True
showHome = True

while inPlay:
    if showHome:
        # Draw the home screen
        home_screen()

        # Home screen loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                score = 0
                health = 3
                spawn_interval = FPS * 2
                bulletX.clear()
                bulletY.clear()
                bulletDirection.clear()
                zombieX.clear()
                zombieY.clear()
                zombieHealth.clear()
                fieldX = CENTER_X - FIELD_SIZE // 2
                fieldY = CENTER_Y - FIELD_SIZE // 2
                showHome = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    # Check for key presses for movements
    if keys[pygame.K_a] and fieldX < CENTER_X - PLAYER_RADIUS:
        fieldX, bulletX, zombieX = shift_left(PLAYER_SPEED, fieldX, bulletX, zombieX)
    if keys[pygame.K_d] and fieldX > CENTER_X - FIELD_SIZE + PLAYER_RADIUS:
        fieldX, bulletX, zombieX = shift_right(PLAYER_SPEED, fieldX, bulletX, zombieX)
    if keys[pygame.K_w] and fieldY < CENTER_Y - PLAYER_RADIUS:
        fieldY, bulletY, zombieY = shift_up(PLAYER_SPEED, fieldY, bulletY, zombieY)
    if keys[pygame.K_s] and fieldY > CENTER_Y - FIELD_SIZE + PLAYER_RADIUS:
        fieldY, bulletY, zombieY = shift_down(PLAYER_SPEED, fieldY, bulletY, zombieY)

    # Add time to reload clock 
    bullet_timer += clock.get_time()

    # Check for mouse clicks for shots within reload time
    if mouse[0] and bullet_timer >= 200:
        chompSound.play()
        bulletX.append(CENTER_X)
        bulletY.append(CENTER_Y)
        mouseX, mouseY = pygame.mouse.get_pos()
        angle = math.atan2(mouseY - CENTER_Y, mouseX - CENTER_X)
        bulletDirection.append((math.cos(angle), math.sin(angle)))
        bullet_timer = 0

    # Move bullets based on direction movement
    for i in range(len(bulletX)):
        bulletX[i] += bulletDirection[i][0] * BULLET_SPEED
        bulletY[i] += bulletDirection[i][1] * BULLET_SPEED

    # Iterate through zombies to check for bullet collisions
    for i in range(len(zombieX) - 1, -1, -1):
        dx = CENTER_X - zombieX[i]
        dy = CENTER_Y - zombieY[i]
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            zombieX[i] += ZOMBIE_SPEED * dx / distance
            zombieY[i] += ZOMBIE_SPEED * dy / distance

        # Go through bullets to check if bullets and zombies are touching
        for e in range(len(bulletX) - 1, -1, -1):
            bullet_dx = bulletX[e] - zombieX[i]
            bullet_dy = bulletY[e] - zombieY[i]
            bullet_distance = math.sqrt(bullet_dx**2 + bullet_dy**2)
            if bullet_distance < BULLET_RADIUS + ZOMBIE_RADIUS:
                zombieHealth[i] -= 1

                # Check if zombie is defeated
                if zombieHealth[i] <= 0:
                    del zombieX[i]
                    del zombieY[i]
                    del zombieHealth[i]
                    score += 1
                    if score > highScore:
                        highScore = score
                    break

                # Delete bullets on impact
                del bulletX[e]
                del bulletY[e]
                del bulletDirection[e]

        if i < len(zombieX):
            if distance < PLAYER_RADIUS + ZOMBIE_RADIUS:
                current_time = pygame.time.get_ticks()
                if current_time - last_hit_time > 1000:
                    health -= 1
                    last_hit_time = current_time

    # Go to game-over screen when played is defeated
    if health <= 0:
        showHome = True
        if not game_over_screen(score, highScore):
            score = 0
            health = 3
            spawn_interval = FPS * 2
            bulletX.clear()
            bulletY.clear()
            bulletDirection.clear()
            zombieX.clear()
            zombieY.clear()
            zombieHealth.clear()
            fieldX = CENTER_X - FIELD_SIZE // 2
            fieldY = CENTER_Y - FIELD_SIZE // 2
            showHome = False

    # Add frame to spawn timer
    spawn_timer += 1

    # Generate zombies with shortening interevals every round
    if spawn_interval > 0:
        spawn_interval -= 0.01
    if spawn_timer >= spawn_interval:
        spawn_zombie(fieldX, fieldY)
        spawn_timer = 0

    # Draw the game
    draw_game(gameWindow, fieldX, fieldY, score, highScore, health)

    # Set FPS
    clock.tick(FPS)

# Quit the game
pygame.quit()