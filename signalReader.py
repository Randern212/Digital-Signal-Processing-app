from signalClass import *

def readSignal(filePath:str)->SignalData:
    returnSignal:SignalData = SignalData()

    with open(filePath,'r') as signalFile:
        returnSignal.SignalType=int(signalFile.readline())
        returnSignal.IsPeriodic=int(signalFile.readline())
        returnSignal.N1=int(signalFile.readline())
        for i in range(returnSignal.N1+1):
             line = signalFile.readline()
             
             values = line.split()
             if returnSignal.SignalType == 0:
                if len(values) >= 2:
                    index = int(values[0])
                    amplitude = float(values[1])
                    returnSignal.data[index] = amplitude
             else:
                if len(values) >= 3:
                    frequency = float(values[0])
                    amplitude = float(values[1])
                    phaseShift = float(values[2])
                    returnSignal.data[frequency] = (amplitude, phaseShift)
    
    return returnSignal