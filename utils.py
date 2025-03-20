import numpy as np
from scipy.signal import butter, lfilter, welch
from sklearn.cross_decomposition import CCA

def butter_bandpass(lowcut, highcut, fs, order=4):
    """Creates a Butterworth bandpass filter."""
    nyq = 0.5 * fs  # Nyquist frequency
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut=0.5, highcut=30, fs=250, order=4):
    """Applies a bandpass filter to the EEG data."""
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    filtered_data = lfilter(b, a, data, axis=0)
    return filtered_data

def adaptive_filter(eeg_data, noise_reference, alpha=0.1):
    """Applies an adaptive filter to remove noise from EEG data."""
    if eeg_data.shape != noise_reference.shape:
        raise ValueError("EEG data and noise reference must have the same shape")
    
    filtered_data = eeg_data - alpha * noise_reference
    return filtered_data

def perform_fft(eeg_data, fs=250):
    freqs, psd = welch(eeg_data, fs=fs, nperseg=fs)
    dominant_freq = freqs[np.argmax(psd)]
    return dominant_freq

def perform_cca(eeg_data):
    reference_freqs = [6, 8, 10, 12]  # Target stimulus frequencies
    reference_signals = [
        np.array([np.sin(2 * np.pi * f * np.linspace(0, 1, eeg_data.shape[0])), 
                  np.cos(2 * np.pi * f * np.linspace(0, 1, eeg_data.shape[0]))]).T 
        for f in reference_freqs
    ]
    
    cca = CCA(n_components=1)
    best_freq = None
    highest_correlation = 0
    
    for i, ref in enumerate(reference_signals):
        cca.fit(eeg_data, ref)
        X_c, Y_c = cca.transform(eeg_data, ref)
        correlation = abs(np.corrcoef(X_c.T, Y_c.T)[0, 1])  # Use absolute correlation
        
        if correlation > highest_correlation:
            highest_correlation = correlation
            best_freq = reference_freqs[i]

    print(f"🎯 Best SSVEP Frequency Detected: {best_freq} Hz (Correlation: {highest_correlation:.2f})")
    return best_freq

def extract_p300_epochs(eeg_data, event_timestamps, fs=250, pre_stimulus=100, post_stimulus=600):
    """Extracts P300 epochs from EEG data based on stimulus timestamps."""
    pre_samples = int((pre_stimulus / 1000) * fs)
    post_samples = int((post_stimulus / 1000) * fs)
    
    if not event_timestamps:
        return np.array([])

    epochs = []
    base_time = event_timestamps[0]  # Reference start time
    
    for timestamp in event_timestamps:
        idx = int((timestamp - base_time) * fs)  # Convert absolute to relative index
        if idx - pre_samples > 0 and idx + post_samples < eeg_data.shape[0]:
            epoch = eeg_data[idx - pre_samples : idx + post_samples]
            epochs.append(epoch)

    return np.array(epochs)

def detect_p300(eeg_epochs, threshold=5):
    p300_presence = []
    for epoch in eeg_epochs:
        avg_amplitude = np.mean(epoch)
        p300_presence.append(1 if avg_amplitude > threshold else 0)  # Thresholding (adjust as needed)
    return np.array(p300_presence)
