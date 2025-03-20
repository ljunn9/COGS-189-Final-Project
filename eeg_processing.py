import numpy as np
from pylsl import StreamInlet, resolve_stream
from utils import bandpass_filter, perform_cca, extract_p300_epochs, detect_p300

def connect_to_eeg():
    print("Searching for EEG stream")
    streams = resolve_stream('type', 'EEG')
    
    if not streams:
        raise RuntimeError("No EEG stream found")

    print("EEG stream connected.")
    return StreamInlet(streams[0])

def process_eeg(event_timestamps, fs=250):
    eeg_inlet = connect_to_eeg()
    eeg_data = []

    for _ in range(fs * len(event_timestamps)):  
        sample, _ = eeg_inlet.pull_sample()
        eeg_data.append(sample)

    eeg_data = np.array(eeg_data)

    filtered_data = bandpass_filter(eeg_data)

    ssvep_classification = perform_cca(filtered_data)

    eeg_epochs = extract_p300_epochs(filtered_data, event_timestamps, fs=fs)
    p300_detected = detect_p300(eeg_epochs)

    return ssvep_classification, p300_detected
