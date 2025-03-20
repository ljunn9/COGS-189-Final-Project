import numpy as np
from scipy.signal import butter, lfilter, welch
from sklearn.cross_decomposition import CCA

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut=6, highcut=15, fs=250, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return lfilter(b, a, data, axis=0)

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
