import numpy as np
from scipy.signal import butter, lfilter, welch
from sklearn.cross_decomposition import CCA
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import seaborn as sns

def bandpass_filter(data, lowcut=2, highcut=40, fs=250, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band'
    filtered_data = lfilter(b, a, data, axis=0)
    return filtered_data

def adaptive_filter(eeg_data, noise_ref, alpha=0.1):
    filtered_data = eeg_data - alpha * noise_ref
    return filtered_data

def perform_fft(eeg_data, fs=250):
    freqs, psd = welch(eeg_data, fs=fs, nperseg=fs)
    dominant_freq = freqs[np.argmax(psd)]
    return dominant_freq

def perform_cca(eeg_data):
    reference_freqs = [6, 8, 10, 12] 
    reference_signals = [
        np.array([np.sin(2 * np.pi * f * np.linspace(0, 1, eeg_data.shape[0])), 
                  np.cos(2 * np.pi * f * np.linspace(0, 1, eeg_data.shape[0]))]).T 
        for f in reference_freqs
    ]
    
    cca = CCA(n_components=1)
    correlations = []
    for ref in reference_signals:
        cca.fit(eeg_data, ref)
        X_c, Y_c = cca.transform(eeg_data, ref)
        correlations.append(np.corrcoef(X_c.T, Y_c.T)[0, 1])
        return np.argmax(correlations)

def classify_ssvep_combined(eeg_data, fs=250):
    fft_classification = perform_fft(eeg_data, fs)
    cca_classification = perform_cca(eeg_data, fs)

    if abs(fft_classification - cca_classification) < 1.5:  
        return cca_classification  
    else:
        return fft_classification
        
def extract_p300_epochs(eeg_data, event_timestamps, fs=250, pre_stimulus=100, post_stimulus=600):
    pre_samples = int((pre_stimulus / 1000) * fs)
    post_samples = int((post_stimulus / 1000) * fs)
    epochs = []
    if not event_timestamps:
        return np.array([])
        
    base_time = event_timestamps[0]

    for timestamp in event_timestamps:
        idx = int((timestamp - base_time) * fs)
        if idx - pre_samples > 0 and idx + post_samples < len(eeg_data):
            epochs.append(eeg_data[idx - pre_samples : idx + post_samples])
    return np.array(epochs)

def detect_p300(eeg_epochs, threshold=5):
    return ["detected" if np.mean(epoch) > threshold else "undetected" for epoch] 

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
