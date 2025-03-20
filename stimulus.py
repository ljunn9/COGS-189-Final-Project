import time
import pygame
import random
from pylsl import StreamInfo, StreamOutlet
from config import STIMULUS_POSITIONS

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SSVEP + P300 Stimuli")

info = StreamInfo(name="Markers", type="Markers", channel_count=1, channel_format="int32", source_id="stimulus_markers")
marker_outlet = StreamOutlet(info)

def flicker_stimuli(num_trials=20, trial_duration=5):
    """Displays SSVEP + P300 stimuli and sends LSL event markers"""
    running = True
    clock = pygame.time.Clock()
    flicker_state = {key: True for key in STIMULUS_POSITIONS}
    event_timestamps = []
    
    trial_count = 0
    while trial_count < num_trials:  
        trial_start = time.time()
        
        while time.time() - trial_start < trial_duration:  
            screen.fill((0, 0, 0))
            p300_target = random.choice(list(STIMULUS_POSITIONS.keys()))  
            event_timestamps.append((time.time(), p300_target))
            
            marker_outlet.push_sample([p300_target])

            for key, stim in STIMULUS_POSITIONS.items():
                if flicker_state[key]:
                    color = (255, 255, 255) if key != p300_target else (0, 255, 0)
                    pygame.draw.circle(screen, color, stim["pos"], 50)

                if time.time() % (1 / stim["freq"]) < (1 / (2 * stim["freq"])):
                    flicker_state[key] = not flicker_state[key]

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
        
        trial_count += 1  

    pygame.quit()
    return event_timestamps
