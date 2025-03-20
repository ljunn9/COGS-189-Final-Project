from stimulus import flicker_stimuli
from eeg_processing import process_eeg
from cursor_control import control_cursor
import threading

def main():
    # Run visual stimuli in a separate thread
    stimulus_thread = threading.Thread(target=flicker_stimuli)
    stimulus_thread.start()

    # Start EEG processing and cursor control
    while True:
        eeg_data = process_eeg()
        control_cursor(eeg_data)

if __name__ == "__main__":
    main()
