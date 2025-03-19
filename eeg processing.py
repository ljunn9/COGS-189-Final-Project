import numpy as np
from pylsl import StreamInlet, resolve_byprop
from utils import bandpass_filter, perform_fft, adaptive_filter, perform_cca
from config import ELECTRODE_INDICES, FS

def connect_to_eeg():
    print("Looking for an EEG stream...")
    streams = resolve_byprop('type', 'EEG', timeout=5)
    if len(streams) == 0:
        raise RuntimeError("No EEG stream found.")
    return StreamInlet(streams[0])

inlet = connect_to_eeg()

def process_eeg():
    eeg_data = []
    timestamps = []
    start_time = time.time()

    # Collect EEG data for 1 second
    while time.time() - start_time < 1:
        sample, timestamp = inlet.pull_sample()
        eeg_data.append([sample[i] for i in ELECTRODE_INDICES])
        timestamps.append(timestamp)

    eeg_data = np.array(eeg_data)

    # Apply band-pass filtering
    eeg_data = bandpass_filter(eeg_data)

    # Apply adaptive noise reduction
    noise_reference = np.mean(eeg_data, axis=0)
    eeg_data = adaptive_filter(eeg_data, noise_reference)

    # Perform FFT to detect dominant SSVEP frequency
    dominant_freq = perform_fft(eeg_data)

    # Classify using CCA
    classification = perform_cca(eeg_data)

    return classification
4️⃣ cursor_control.py (Cursor Movement)
Moves cursor in real-time based on SSVEP classification.

python
Copy code
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
