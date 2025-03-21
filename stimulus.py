import time
import pygame
import random
from config import STIMULUS_POSITIONS
from pylsl import StreamInfo, StreamOutlet

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SSVEP + P300 Stimuli")

info = StreamInfo(name='Markers', type='Markers', channel_count=1, channel_format='int32', source_id='stimulus_markers')
outlet = StreamOutlet(info)

TRIAL_DURATION = 5  
P300_FLASH_DURATION = 0.1  
P300_FLASH_INTERVAL = 0.4  
SSVEP_FREQUENCIES = [6, 8, 10, 12] 

def flicker_stimuli(num_trials=20, trial_duration=5):
    running = True
    clock = pygame.time.Clock()
    flicker_state = {key: True for key in STIMULUS_POSITIONS}
    event_timestamps = []
    trial_count = 0 
    while trial_count < num_trials:
        print(f"Trial {trial + 1}/{num_trials} started")
        trial_start = time.time()
        
        while time.time() - trial_start < TRIAL_DURATION:  
            screen.fill((0, 0, 0))        
            p300_target = random.choice(list(STIMULUS_POSITIONS.keys()))  
            event_timestamps.append((time.time(), p300_target))
            print(f"Sending marker: {p300_target} at {time.time()}")
            outlet.push_sample([p300_target])

            for key, stim in STIMULUS_POSITIONS.items():
                if flicker_state[key]:
                    color = (255, 255, 255) if key != p300_target else (0, 255, 0)
                    pygame.draw.circle(screen, color, stim["pos"], 50)

                if time.time() % (1 / stim["freq"]) < (1 / (2 * stim["freq"])):
                    flicker_state[key] = not flicker_state[key]  
                    
            pygame.display.flip()
            clock.tick(60)
            time.sleep(P300_FLASH_DURATION)

        time.sleep(P300_FLASH_INTERVAL)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        

    pygame.quit()
    return event_timestamps
