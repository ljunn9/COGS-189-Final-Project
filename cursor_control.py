import time
from pylsl import StreamInfo, StreamOutlet

info = StreamInfo(name='KeyboardControl', type='Control', channel_count=1, channel_format='string', source_id='keyboard_control')
outlet = StreamOutlet(info)

KEYBOARD_LAYOUT = [
    ["Q", "W", "E", "R", "T", "Y"],
    ["A", "S", "D", "F", "G", "H"],
    ["Z", "X", "C", "V", "B", "N"],
    ["1", "2", "3", "4", "5", "6"],
]

def type_character(row, col):
    letter = KEYBOARD_LAYOUT[row][col]
    outlet.push_sample([letter]) 
    print(f" Typed Letter: {letter}")

def control_keyboard(ssvep_classification, p300_detected):
    if p300_detected:
        row = ssvep_classification // 6  
        col = ssvep_classification % 6  
        type_character(row, col)
