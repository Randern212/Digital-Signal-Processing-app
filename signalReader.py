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

def writeSignal(signal: SignalData,index:int):
    filePath:str="outputSignals//"
    with open(filePath, 'w') as signalFile:
        signalFile.name="Signal"+str(index)
        signalFile.write(f"{int(signal.SignalType)}\n")
        signalFile.write(f"{int(signal.IsPeriodic)}\n")
        signalFile.write(f"{signal.N1}\n")
        
        if signal.SignalType == 0:
            sorted_items = sorted(signal.data.items(), key=lambda x: x[0])
            for index, amplitude in sorted_items:
                signalFile.write(f"{index} {amplitude}\n")
        else:  
            sorted_items = sorted(signal.data.items(), key=lambda x: x[0])
            for frequency, (amplitude, phase_shift) in sorted_items:
                signalFile.write(f"{frequency} {amplitude} {phase_shift}\n")