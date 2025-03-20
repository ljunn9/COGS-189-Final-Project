import numpy as np
from scipy.signal import butter, lfilter, welch
from sklearn.cross_decomposition import CCA

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def adaptive_filter(eeg_data, noise_ref):
    step_size = 0.001  # Learning rate for the adaptive filter
    weights = np.zeros(len(noise_ref))
    output = np.zeros(len(eeg_data))

    for i in range(len(eeg_data)):
        y = np.dot(weights, noise_ref[i])
        e = eeg_data[i] - y
        weights += step_size * e * noise_ref[i]
        output[i] = e

    return output

def perform_fft(eeg_data, fs=250):
    freqs, psd = welch(eeg_data, fs=fs, nperseg=fs)
    dominant_freq = freqs[np.argmax(psd)]
    return dominant_freq

def perform_cca(eeg_data):
    reference_freqs = [6, 8, 10, 12]
    reference_signals = [np.array([np.sin(2 * np.pi * f * np.linspace(0, 1, 250)), 
                                   np.cos(2 * np.pi * f * np.linspace(0, 1, 250))]).T for f in reference_freqs]
    cca = CCA(n_components=1)
    correlations = []
    for ref in reference_signals:
        cca.fit(eeg_data, ref)
        X_c, Y_c = cca.transform(eeg_data, ref)
        correlations.append(np.corrcoef(X_c.T, Y_c.T)[0, 1])
    return np.argmax(correlations)
