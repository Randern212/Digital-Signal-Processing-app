from enum import *

class FilterType(Enum):
    LOW = 0
    HIGH = 1
    BAND_PASS = 2
    BAND_STOP = 3

class Filter:
    def __init__(self):
        self.filterType: FilterType = 0
        self.FS = 0
        self.stopBandAttenuation = 0  
        self.F1 = 0
        self.F2 = 0
        self.FC = 0
        self.transitionBand = 0
