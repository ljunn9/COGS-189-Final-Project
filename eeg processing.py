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

    while time.time() - start_time < 1:
        sample, timestamp = inlet.pull_sample()
        eeg_data.append([sample[i] for i in ELECTRODE_INDICES])
        timestamps.append(timestamp)

    eeg_data = np.array(eeg_data)

    eeg_data = bandpass_filter(eeg_data)
    noise_reference = np.mean(eeg_data, axis=0)
    eeg_data = adaptive_filter(eeg_data, noise_reference)
    eeg_data = perform_fft(eeg_data)
    classification = perform_cca(eeg_data)

    return classification
