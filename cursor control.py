import pygame
from config import CURSOR_MOVEMENT

pygame.init()
screen = pygame.display.set_mode((800, 600))
cursor_x, cursor_y = 400, 300

def control_cursor(classification):
    global cursor_x, cursor_y

    # Map classification result to movement direction
    if classification == 0:  # 6 Hz → Up
        cursor_y -= CURSOR_MOVEMENT
    elif classification == 1:  # 8 Hz → Down
        cursor_y += CURSOR_MOVEMENT
    elif classification == 2:  # 10 Hz → Left
        cursor_x -= CURSOR_MOVEMENT
    elif classification == 3:  # 12 Hz → Right
        cursor_x += CURSOR_MOVEMENT

    # Ensure cursor stays within screen bounds
    cursor_x = max(0, min(800, cursor_x))
    cursor_y = max(0, min(600, cursor_y))

    # Update screen
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (0, 255, 0), (cursor_x, cursor_y), 10)
    pygame.display.flip()
