class SignalData:
    SignalType:bool
    IsPeriodic:bool
    N1:int
    data:dict = {}


# The file will contain the samples in time domain or frequency domain,
# Follows is a description for how to build such a file:
# -----------------------------------------------------------------------------
# [SignalType] // Time-->0/Freq-->1
# [IsPeriodic] // takes 0 or 1
# [N1] // number of samples to follow or number of frequencies to follow 
# [Index SampleAmp] or [Freq Amp PhaseShift]// N1 rows follow with Sample Index followed by space followed by Sample Amplitude in case Time domain was specified in the first row in the file,
#  or N1 rows follow with frequency followed by space followed by amplitude followed by Phase shift


# example file.. 
# 0
# 0
# 4
# 0 1 
# 1 2
# 2 3
# 3 4

