import pygame
import time
from config import STIMULUS_POSITIONS

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SSVEP Stimuli")

def flicker_stimuli():
    running = True
    clock = pygame.time.Clock()
    flicker_state = {key: True for key in STIMULUS_POSITIONS}

    while running:
        screen.fill((0, 0, 0))

        for key, stim in STIMULUS_POSITIONS.items():
            if flicker_state[key]:
                pygame.draw.circle(screen, (255, 255, 255), stim["pos"], 50)
            
            if time.time() % (1 / stim["freq"]) < (1 / (2 * stim["freq"])):
                flicker_state[key] = not flicker_state[key]

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
