from stimulus import flicker_stimuli
from eeg_processing import process_eeg
from cursor_control import control_cursor
import threading

def main():
    stimulus_thread = threading.Thread(target=flicker_stimuli) # Start visual stimulus in a separate thread
    stimulus_thread.start()

    while True:
        eeg_data = process_eeg()
        control_cursor(eeg_data)

if __name__ == "__main__":
    main()
