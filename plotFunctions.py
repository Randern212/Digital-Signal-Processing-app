import  matplotlib as plt
from matplotlib import pyplot as pplt
from signalClass import *

def discreteRepresentation(signal:SignalData,step:float=1.0):
    indices=list(signal.data.keys())
    if signal.SignalType==0:
        data =list(signal.data.values())
        pplt.figure(figsize=(100,100))
        stemlines = pplt.stem(indices,data)
        pplt.setp(stemlines ,linewidth=0.5)
        pplt.xlabel('indices')
        pplt.ylabel('amplitudes')
        pplt.title('discrete representation of a time domain signal')
        pplt.show()
    else:
        amplitudes = []
        phases = []
        frequencies=[]

        for key in indices:
            amp,phase = signal.data[key]
            frequencies.append(key*step)
            amplitudes.append(amp)
            phases.append(phase)
        
        pplt.figure(figsize=(100,100))
        stemlines = pplt.stem(frequencies, amplitudes)
        pplt.setp(stemlines ,linewidth=0.5)
        pplt.xlabel('frequencies')
        pplt.ylabel('amplitudes')
        pplt.title('discrete representation of a frequency domain signal (F vs A)')
        pplt.show()
        stemlines = pplt.stem(frequencies,phases)
        pplt.setp(stemlines ,linewidth=0.5)
        pplt.xlabel('frequencies')
        pplt.ylabel('phases')
        pplt.title('discrete representation of a frequency domain signal (F vs THETA)')
        pplt.show()
        
def continousRepresentation(signal:SignalData):
    indices=list(signal.data.keys())
    data =list(signal.data.values())
    if signal.SignalType==0:
        pplt.figure(figsize=(100,100))
        pplt.plot(indices,data)
        pplt.xlabel('indices')
        pplt.ylabel('amplitudes')
        pplt.title('discrete representation of a time domain signal')
        pplt.show()
