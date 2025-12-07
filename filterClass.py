from enum import *

class FilterType(Enum):
    LOW = "low pass"
    HIGH = "high pass"
    BAND_PASS = "band pass"
    BAND_STOP = "band stop"

class Filter:
    def __init__(self):
        self.filterType: FilterType = 0
        self.FS = 0
        self.stopBandAttenuation = 0  
        self.F1 = 0
        self.F2 = 0
        self.FC = 0
        self.transitionBand = 0
