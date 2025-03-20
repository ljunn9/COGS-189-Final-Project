from stimulus import flicker_stimuli
from eeg_processing import process_eeg
from cursor_control import control_cursor
import threading

def main():
    event_timestamps = flicker_stimuli()

    while True:
        ssvep_classification, p300_detected = process_eeg(event_timestamps)
        control_cursor(ssvep_classification, p300_detected)

if __name__ == "__main__":
    main()
