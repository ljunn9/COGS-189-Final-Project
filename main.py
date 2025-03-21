import time
import numpy as np
from stimulus import flicker_stimuli
from eeg_processing import connect_to_eeg, bandpass_filter, classify_ssvep_combined, extract_p300_epochs, detect_p300
from cursor_control import control_keyboard
from utils import initialize_results_file, log_results, visualize_results

initialize_results_file()

eeg_inlet = connect_to_eeg()
event_timestamps = flicker_stimuli(num_trials=10, trial_duration=5)

for trial in range(10):
    print(f" Running Trial {trial+1}/10")

    sample, _ = eeg_inlet.pull_sample()
    if sample is None:
        print("No EEG data received")
        
print(f"✅ EEG Sample Received: {sample}")
        continue 
        
    filtered_data = both_filters(np.array(sample))    
    ssvep_classification = classify_ssvep_combined(filtered_data)
    eeg_epochs = extract_p300_epochs(filtered_data, event_timestamps)
    p300_detected = any(detect_p300(eeg_epochs))
    control_keyboard(ssvep_classification, p300_detected)
    log_results(trial, ssvep_classification, p300_detected, typed_letter)
    time.sleep(1)

print("Experiment Done")
visualize_results()
