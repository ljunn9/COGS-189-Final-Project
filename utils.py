import numpy as np
from scipy.signal import butter, lfilter, welch
from sklearn.cross_decomposition import CCA
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from pylsl import StreamInlet, resolve_byprop

def both_filters(eeg_data, noise_ref, lowcut=2, highcut=40, fs=250, order=4, alpha=0.1):
    # Check for sufficient length
    if eeg_data is None or eeg_data.shape[0] < 2:
        raise ValueError("EEG data too short to apply filters.")
    
    # Check shape compatibility
    if eeg_data.shape != noise_ref.shape:
        raise ValueError("Shape mismatch: EEG data and noise reference must have the same shape.")
    
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    bandpassed_data = lfilter(b, a, eeg_data, axis=0)
    filtered_data = bandpassed_data - alpha * noise_ref
    return filtered_data

def perform_fft(filtered_data, fs=250):
    if filtered_data is None or len(filtered_data) < 2:
        raise ValueError("Error: Input signal is too short for FFT computation.")
    
    if np.var(filtered_data) < 1e-6:
        raise ValueError("Error: Input signal is flat, FFT cannot extract meaningful frequencies.")
    
    segment_size = min(fs, len(filtered_data))
    freqs, psd = welch(filtered_data, fs=fs, nperseg=segment_size)
    dominant_freq = freqs[np.argmax(psd)]
    return dominant_freq

def perform_cca(filtered_data):
    if filtered_data is None or filtered_data.shape[0] < 2:
        raise ValueError("Error: Input signal is too short for CCA computation.")
    
    reference_freqs = [6, 8, 10, 12] 
    num_samples = filtered_data.shape[0]
    
    reference_signals = [
        np.array([
            np.sin(2 * np.pi * f * np.linspace(0, 1, num_samples)), 
            np.cos(2 * np.pi * f * np.linspace(0, 1, num_samples))
        ]).T 
        for f in reference_freqs
    ]

    if filtered_data.ndim == 1:
        filtered_data = filtered_data.reshape(-1, 1)

    cca = CCA(n_components=1)
    correlations = []
    for ref in reference_signals:
        if ref.shape[0] != filtered_data.shape[0]:
            ref = ref[:filtered_data.shape[0], :]
        
        cca.fit(filtered_data, ref)
        X_c, Y_c = cca.transform(filtered_data, ref)
        
        if X_c.shape[0] > 1:
            corr = np.corrcoef(X_c.T, Y_c.T)[0, 1]
        else:
            corr = 0
        
        correlations.append(corr)
    
    if not correlations:
        raise ValueError("No valid correlations computed for CCA.")
    
    return np.argmax(correlations)

def classify_ssvep_combined(filtered_data):
    fs = 250
    reference_freqs = [6, 8, 10, 12]

    if filtered_data is None or filtered_data.shape[0] < 2:
        raise ValueError("Input signal is too short for classification.")

    # Average across channels if multi-channel
    if filtered_data.ndim > 1:
        filtered_data = np.mean(filtered_data, axis=1)
    
    fft_classification = perform_fft(filtered_data, fs)
    cca_classification = reference_freqs[perform_cca(filtered_data)]

    if abs(fft_classification - cca_classification) < 1.5:
        return cca_classification
    else:
        return fft_classification
        
def extract_p300_epochs(eeg_data, event_timestamps, fs=250, pre_stimulus=100, post_stimulus=600):
    pre_samples = int((pre_stimulus / 1000) * fs)
    post_samples = int((post_stimulus / 1000) * fs)
    epochs = []
    if len(event_timestamps) == 0:
        return np.array([])
        
    base_time = event_timestamps[0]

    for timestamp in event_timestamps:
        idx = int((timestamp - base_time) * fs)
        if idx - pre_samples < 0 or idx + post_samples >= len(eeg_data):
            print(f"⚠️ Skipping event at {timestamp}s (out of range)")
            continue
        epochs.append(eeg_data[idx - pre_samples : idx + post_samples])
    return np.array(epochs)

def detect_p300(eeg_epochs, threshold=5):
    if len(eeg_epochs) == 0:
        return []
    return ["detected" if np.mean(epoch) > threshold else "undetected" for epoch in eeg_epochs] 

def connect_to_eeg():
    print("Searching for EEG stream")
    streams = resolve_byprop('type', 'EEG')
    
    if not streams:
        raise RuntimeError("No EEG stream found")

    print("EEG stream connected.")
    return StreamInlet(streams[0])

def process_eeg(event_timestamps, fs=250):
    eeg_inlet = connect_to_eeg()
    eeg_data = []
    print("Collecting EEG data")

    for _ in range(fs * len(event_timestamps)):  
            sample, _ = eeg_inlet.pull_sample()
            eeg_data.append(sample)

    eeg_data = np.array(eeg_data)
    noise_ref = np.mean(eeg_data, axis=0)  # Estimate noise from EEG channels
    filtered_data = both_filters(eeg_data, noise_ref)
    ssvep_classification = classify_ssvep_combined(filtered_data)
    eeg_epochs = extract_p300_epochs(filtered_data, event_timestamps)
    p300_detected = detect_p300(eeg_epochs)

    return ssvep_classification, p300_detected

RESULTS_FILE = "keyboard_control_results.csv"

def initialize_results_file():
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Trial", "SSVEP Classification", "P300 Detected", "Typed Letter"])

def log_results(trial, ssvep_classification, p300_detected, typed_letter):
    with open(RESULTS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([trial, ssvep_classification, p300_detected, typed_letter])

def visualize_results():
    df = pd.read_csv(RESULTS_FILE)
    
    accuracy = df["P300 Detected"].mean() * 100 
    print(accuracy)

    plt.figure(figsize=(6, 4))
    sns.barplot(x=["No P300", "P300 Detected"], y=df["P300 Detected"].value_counts().values)
    plt.title(f"P300 Detection Rate ({accuracy:.2f}% Accuracy)")
    plt.ylabel("Number of Trials")
    plt.show()

    plt.figure(figsize=(8, 6))
    sns.histplot(df["SSVEP Classification"], bins=24, kde=True)
    plt.title("SSVEP Classification Distribution")
    plt.xlabel("Classified Letter (Index)")
    plt.ylabel("Frequency")
    plt.show()
