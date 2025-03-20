import time
import numpy as np
from stimulus import flicker_stimuli
from eeg_processing import connect_to_eeg, bandpass_filter, classify_ssvep_combined, extract_p300_epochs, detect_p300
from cursor_control import control_keyboard

# Start LSL EEG Stream
eeg_inlet = connect_to_eeg()
event_timestamps = flicker_stimuli()

for trial in range(100):
    print(f" Running Trial {trial+1}/100")

    sample, _ = eeg_inlet.pull_sample()
    filtered_data = bandpass_filter(np.array(sample))
    
    sample, _ = eeg_inlet.pull_sample(timeout=2.0) 
    if sample is None:
        print("No EEG data received")
        continue  

    ssvep_classification = classify_ssvep_combined(filtered_data)
    eeg_epochs = extract_p300_epochs(filtered_data, event_timestamps)
    p300_detected = any(detect_p300(eeg_epochs))

    control_keyboard(ssvep_classification, p300_detected)
    time.sleep(1)

print("Experiment Done")
