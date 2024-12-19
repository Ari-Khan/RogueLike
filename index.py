import pygame
import math

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
WHITE = (0, 0, 0)
LIGHT_GREEN = (60, 255, 80)
DARK_GREEN = (0, 100, 0) 
BLUE = (50, 100, 250)

PLAYER_RADIUS = 30
BULLET_RADIUS = 5
BULLET_SPEED = 10

# Setup display
gameWindow = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Movement Example")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Camera offset (initially centered on the player)
fieldX = CENTER_X - FIELD_SIZE // 2
fieldY = CENTER_Y  - FIELD_SIZE // 2

# Movement speed
speed = 5

mouseX = 0
mouseY = 0

bulletX = []
bulletY = []
bulletDirection = []

# Game drawing function
def draw_game():
    # Clear the screen with a dark green background
    gameWindow.fill(DARK_GREEN)

    # Draw the square background (1000x1000 field)
    pygame.draw.rect(gameWindow, LIGHT_GREEN, (fieldX, fieldY, FIELD_SIZE, FIELD_SIZE))
    
    for i in range(len(bulletX)):
        pygame.draw.circle(gameWindow, WHITE, (bulletX[i], bulletY[i]), BULLET_RADIUS)

    # Draw the player as a circle centered on the screen
    pygame.draw.circle(gameWindow, BLUE, (CENTER_X, CENTER_Y), PLAYER_RADIUS)

    pygame.display.update()

# Game loop
inPlay = True
while inPlay:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False

    # Handle key presses
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and fieldX < CENTER_X - PLAYER_RADIUS:
        fieldX += speed
    if keys[pygame.K_d] and fieldX > CENTER_X - FIELD_SIZE + PLAYER_RADIUS:
        fieldX -= speed
    if keys[pygame.K_w] and fieldY < CENTER_Y - PLAYER_RADIUS:
        fieldY += speed
    if keys[pygame.K_s] and fieldY > CENTER_Y - FIELD_SIZE + PLAYER_RADIUS:
        fieldY -= speed
    if keys[pygame.K_SPACE]:
        bulletX.append(CENTER_X)
        bulletY.append(CENTER_Y)
        mouseX, mouseY = pygame.mouse.get_pos()
        # Calculate angle using atan2
        angle = math.atan2(mouseY - CENTER_Y, mouseX - CENTER_X)
        # Store velocity components (cos for X, sin for Y)
        bulletDirection.append((math.cos(angle), math.sin(angle)))

    # Update bullets
    for i in range(len(bulletX)):
        bulletX[i] += bulletDirection[i][0] * BULLET_SPEED  # X component
        bulletY[i] += bulletDirection[i][1] * BULLET_SPEED  # Y component


    # Call the draw function
    draw_game()

    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()


