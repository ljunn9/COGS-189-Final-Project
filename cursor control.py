import pygame
from config import CURSOR_MOVEMENT

pygame.init()
screen = pygame.display.set_mode((800, 600))
cursor_x, cursor_y = 400, 300

def control_cursor(ssvep_classification, p300_detected):
    global cursor_x, cursor_y

    if p300_detected:
        if ssvep_classification == 0:  # Up
            cursor_y -= CURSOR_MOVEMENT
        elif ssvep_classification == 1:  # Down
            cursor_y += CURSOR_MOVEMENT
        elif ssvep_classification == 2:  # Left
            cursor_x -= CURSOR_MOVEMENT
        elif ssvep_classification == 3:  # Right
            cursor_x += CURSOR_MOVEMENT

    cursor_x = max(0, min(800, cursor_x))
    cursor_y = max(0, min(600, cursor_y))

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (0, 255, 0), (cursor_x, cursor_y), 10)
    pygame.display.flip()
