FS = 250  

ELECTRODE_INDICES = {
    "SSVEP": [0, 1, 2],  
    "P300": [3, 4, 5, 6, 7]  
}

P300_ELECTRODES = ELECTRODE_INDICES["P300"]
SSVEP_ELECTRODES = ELECTRODE_INDICES["SSVEP"]

STIMULUS_POSITIONS = [
    ["Q", "W", "E", "R", "T", "Y"],
    ["A", "S", "D", "F", "G", "H"],
    ["Z", "X", "C", "V", "B", "N"],
    ["1", "2", "3", "4", "5", "6"],
]

CURSOR_MOVEMENT = 20

P300_FLASH_PROBABILITY = 0.2  
P300_FLASH_DURATION = 0.1  
P300_FLASH_INTERVAL = 0.3  


P300_TARGETS = {
    "UP": {"pos": (400, 100)},
    "DOWN": {"pos": (400, 500)},
    "LEFT": {"pos": (100, 300)},
    "RIGHT": {"pos": (700, 300)}
}
