FS = 250  

SSVEP_ELECTRODE_INDICES = [0, 1, 2] 
P300_ELECTRODE_INDICES = [3, 4, 5]  

STIMULUS_POSITIONS = {
    "UP": {"pos": (400, 100), "freq": 6},
    "DOWN": {"pos": (400, 500), "freq": 8},
    "LEFT": {"pos": (100, 300), "freq": 10},
    "RIGHT": {"pos": (700, 300), "freq": 12}
}

CURSOR_MOVEMENT = 20

P300_FLASH_PROBABILITY = 0.2  
P300_FLASH_DURATION = 0.1  
P300_FLASH_INTERVAL = 0.3  

P300_TARGETS = {
    "UP": {"pos": (400, 100)},
    "DOWN": {"pos": (400, 500)},
    "LEFT": {"pos": (100, 300)},
    "RIGHT": {"pos": (700, 300)}
