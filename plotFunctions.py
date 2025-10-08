import  matplotlib as plt
from matplotlib import pyplot as pplt
from signalClass import *

def discreteRepresentation(signal:SignalData):
    indices=list(signal.data.keys())
    data =list(signal.data.values())
    if signal.SignalType==0:
        pplt.figure(figsize=(100,100))
        stemlines = pplt.stem(indices,data)
        pplt.setp(stemlines ,linewidth=0.5)
        pplt.xlabel('indices')
        pplt.ylabel('amplitudes')
        pplt.title('discrete representation of a time domain signal')
        pplt.show()

def continousRepresentation(signal:SignalData):
    pass