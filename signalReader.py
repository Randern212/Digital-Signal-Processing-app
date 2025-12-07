from signalClass import *
from QuantizedSignal import *
from enum import Enum
class WriteMethod(Enum):
    normal=0
    quantizedBits=1
    quantizedLevels=2

class FilterType(Enum):
    LOW = "low pass"
    HIGH = "high pass"
    BAND_PASS = "band pass"
    BAND_STOP = "band stop"

def readSignal(filePath:str,skipFrequency:bool=False)->SignalData:
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
                if skipFrequency and len(values)>=2:
                    amplitude = float(values[0].rstrip('f'))
                    phaseShift = float(values[1].rstrip('f'))
                    returnSignal.data[i] = (amplitude, phaseShift)
                if len(values) >= 3:                
                    frequency = float(values[0])
                    amplitude = float(values[1])
                    phaseShift = float(values[2])
                    returnSignal.data[frequency] = (amplitude, phaseShift)

    return returnSignal

def writeSignal(signal, index:int, mode:WriteMethod = WriteMethod.normal, numberOfBits:int = 0):
    filePath:str="Signal"+str(index)+".txt"
    with open(filePath, 'w') as signalFile:
        signalFile.write(f"{int(signal.SignalType)}\n")
        signalFile.write(f"{int(signal.IsPeriodic)}\n")
        signalFile.write(f"{signal.N1}\n")
        match mode:
            case WriteMethod.normal:
                writeModeNoraml(signal,signalFile)
            case WriteMethod.quantizedBits:
                writeModeQuantizedBits(signal,signalFile,numberOfBits)
            case WriteMethod.quantizedLevels:
                writeModeQuantizedLevels(signal,signalFile,numberOfBits)

def writeModeNoraml(signal,signalFile):
    if signal.SignalType == 0:
        sortedItems = sorted(signal.data.items(), key=lambda x: x[0])
        for i, amplitude in sortedItems:
            signalFile.write(f"{i} {amplitude}\n")
    else:  
        sortedItems = sorted(signal.data.items(), key=lambda x: x[0])
        for  frequency, (amplitude, phaseShift) in sortedItems:
            signalFile.write(f"{frequency} {amplitude} {phaseShift}\n")

def writeModeQuantizedBits(signal, signalFile, numberOfBits:int):
    if signal.SignalType == 0:
        for level,amplitude in signal.data:
            encodedLevel=format(level,'#0'+str(numberOfBits+2)+'b')[2:]
            signalFile.write(f"{encodedLevel} {amplitude}\n")

def writeModeQuantizedLevels(signal, signalFile, numberOfBits:int):
    if signal.SignalType == 0:
        i:int=0
        for level,amplitude in signal.data:
            encodedLevel=format(level,'#0'+str(numberOfBits+2)+'b')[2:]
            signalFile.write(f"{level+1} {encodedLevel} {amplitude} {signal.error[i]}\n")
            i+=1

def readFilter(filePath:str):
    filterTypeMap = {
        "low pass": FilterType.LOW,
        "high pass": FilterType.HIGH,
        "band pass": FilterType.BAND_PASS,
        "band stop": FilterType.BAND_STOP,
    }
    with open(filePath) as f:
        lines = [line.strip().split('=') for line in f if '=' in line]
        parameters = {k.strip(): v.strip() for k, v in lines}
    
    fs = int(parameters['FS'])
    stopBandAttenuation = int(parameters['StopBandAttenuation'])
    transitionBand = int(parameters['TransitionBand'])

    filterType=filterTypeMap[parameters['FilterType'].lower()]
    
    if filterType==FilterType.BAND_PASS or filterType==FilterType.BAND_STOP:
        f1 = float(parameters['F1'])
        f2 = float(parameters['F2'])
        return filterType, fs, stopBandAttenuation, (f1 ,f2), transitionBand
    
    fc= float(parameters['FC'])

    return filterType, fs, stopBandAttenuation, fc, transitionBand