class QuantizedSignal:
    def __init__(self):
        self.SignalType: bool = False
        self.IsPeriodic: bool = False  
        self.N1: int = 0
        self.data:list[tuple[int,float]]=[]

# The file will contain the samples in time domain or frequency domain,
# Follows is a description for how to build such a file:
# -----------------------------------------------------------------------------
# [SignalType] // Time-->0/Freq-->1
# [IsPeriodic] // takes 0 or 1
# [N1] // number of samples to follow or number of frequencies to follow 
# [bitSizedLevel SampleAmp] N1 rows 

# example file.. 
# 0
# 0
# 11
# 001 0.35
# 010 0.45
# 010 0.45
# 011 0.55
# 011 0.55
# 100 0.65
# 101 0.75
# 110 0.85
# 110 0.85
# 111 0.95
# 000 0