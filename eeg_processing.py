import numpy as np
import time
from pylsl import StreamInlet, resolve_byprop
from utils import bandpass_filter, perform_fft, adaptive_filter, perform_cca, extract_p300_epochs, detect_p300
from config import FS, ELECTRODE_INDICES, P300_ELECTRODES

def connect_to_eeg():
    print("Looking for an EEG stream...")
    streams = resolve_byprop('type', 'EEG', timeout=5)
    if len(streams) == 0:
        raise RuntimeError("No EEG stream found.")
    return StreamInlet(streams[0])

inlet = connect_to_eeg()

def process_eeg(event_timestamps):
    eeg_data = []
    timestamps = []
    start_time = time.time()

    while time.time() - start_time < duration:
        sample, timestamp = inlet.pull_sample()
       if sample:
           eeg_data.append(sample)
           timestamps.append(timestamp)

    eeg_data = np.array(eeg_data)
    
    eeg_data = bandpass_filter(eeg_data) # Apply bandpass filtering

    
    noise_reference = np.mean(eeg_data, axis=0) # Apply adaptive noise reduction
    eeg_data = adaptive_filter(eeg_data, noise_reference)

    dominant_freq = perform_fft(eeg_data) # Perform FFT for SSVEP feature extraction

    ssvep_classification = perform_cca(eeg_data) # Classify SSVEP using CCA

    p300_epochs = extract_p300_epochs(eeg_data, event_timestamps) # Extract and classify P300 epochs
    p300_detected = detect_p300(p300_epochs)

    return ssvep_classification, p300_detected
