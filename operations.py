from tkinter import *
from enum import Enum
from buttonFunctions import *
from signalReader import *
import math
from QuantizedSignal import *
from plotFunctions import *
from cmath import *
class operation(Enum):
    addition=0
    subtraction=1

class signalType(Enum):
    sin=0
    cosine=1

class quantizationType(Enum):
    bits=0
    levels=1

def addSignals():
    global signalList
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType = signalList[0].SignalType
    resultantSignal.IsPeriodic = all(signal.IsPeriodic for signal in signalList)
    for i in range(max(signalList,key=lambda signal:signal.N1).N1):
        res:float=0
        for signal in signalList:
            res+=signal.data[i]
        resultantSignal.data[i]=res
    signalList=[]

    return resultantSignal


def subtractSignals():
    global signalList
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType = signalList[0].SignalType
    resultantSignal.IsPeriodic = all(signal.IsPeriodic for signal in signalList)
    for i in range(max(signalList,key=lambda signal:signal.N1).N1):
        sub:float = max(signalList,key=lambda signal:signal.data[i]).data[i]
        index:int = signalList.index(max(signalList,key=lambda signal:signal.data[i]))
        for signal in signalList:
            if signalList.index(signal)==index:
                continue
            else:
                sub-=signal.data[i]
        resultantSignal.data[i]=sub
    signalList=[]

    return resultantSignal

def multiplySignal(signal:SignalData,constant:float,write:bool=True):
    global signalCounter
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1
    for index in signal.data.keys():
        resultantSignal.data[index]=signal.data[index]*constant
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1

    return resultantSignal

def squareSignal(signal:SignalData,write:bool=True):
    global signalCounter
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1
    for index in signal.data.keys():
        resultantSignal.data[index]=signal.data[index]*signal.data[index]
    
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
    
    return resultantSignal

def accumulateSignal(signal:SignalData, write:bool=True):
    global signalCounter
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1
    resSum:float=0
    for index in signal.data.keys():
        resSum+=signal.data[index]
        resultantSignal.data[index]=resSum
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1

    return resultantSignal

def calculate(mode:operation,write:bool=True):
    global signalCounter
    resultantSignal=None
    match mode:
        case operation.addition:
            resultantSignal=addSignals()
        case operation.subtraction:
            resultantSignal=subtractSignals()
    
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1

    return resultantSignal

def normalizeMinMax(signal:SignalData,write:bool=True):
    global signalCounter
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1

    amplitudes = [signal.data[i] for i in range(signal.N1)]
    maxValue:float=max(amplitudes)
    minValue:float=min(amplitudes)

    for index in signal.data.keys():
        resultantSignal.data[index]=(signal.data[index]-minValue)/(maxValue-minValue)
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1

    return resultantSignal

def normalizePeak(signal:SignalData, write:bool=True):
    global signalCounter
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1

    if resultantSignal.SignalType==0:
        maxValue:float=abs(max(signal.data.values()))

        for index in signal.data.keys():
            resultantSignal.data[index]=signal.data[index]/maxValue
    else:
        maxValue:float=abs(max(signal.data.values(),key=lambda pair:pair[0])[0])

        for frequency,(amplitude,phase) in signal.data.items():
            resultantSignal.data[frequency]=(amplitude/maxValue,phase)

    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1

    return resultantSignal

def generateSignal(amplitude:float,phaseShift:float,analogF:float,samplingF:float,trigFunc:callable):
    global signalCounter
    resultantSignal = SignalData()
    resultantSignal.SignalType = 0  
    resultantSignal.IsPeriodic = 1
    
    samplingInterval = 1.0 / samplingF
    resultantSignal.N1 = samplingF
    
    for n in range(int(samplingF)):
        t = n * samplingInterval
        sampleValue = amplitude * trigFunc(2 * math.pi * analogF * t + phaseShift)
        resultantSignal.data[n] = sampleValue

    writeSignal(resultantSignal,signalCounter)
    signalCounter+=1

def quantizeSignalByBits(signal:SignalData,numberOfBits:int,write:bool=True):
    global signalCounter
    resultantSignal = QuantizedSignal()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1

    numberOfLevels:int= 2**(numberOfBits)
    amplitudes = [signal.data[i] for i in range(signal.N1)]

    maxValue:float=max(amplitudes)
    minValue:float=min(amplitudes)

    Delta:float=(maxValue-minValue)/numberOfLevels

    ranges, midpoints = createRanges(numberOfLevels, minValue, maxValue, Delta)
    
    for index in range(signal.N1):
        originalAmplitude=signal.data[index]
        quantizedAmplitude, currentLevel=estimateIndex(originalAmplitude, ranges, midpoints)
        quantizationError:float=quantizedAmplitude - originalAmplitude    
        resultantSignal.data.append((currentLevel, quantizedAmplitude))
        resultantSignal.error.append(quantizationError)

    if write:
        writeSignal(resultantSignal,signalCounter,WriteMethod.quantizedBits,numberOfBits)
        signalCounter+=1
    
    return resultantSignal

def estimateIndex(amplitude:int, rangeList:list[tuple[float,float]], midpointsList:list[float]):
    quantizedAmplitude = amplitude
    currentLevel=0
    for i in range(len(midpointsList)):
        if quantizedAmplitude>=rangeList[i][0] and quantizedAmplitude<=rangeList[i][1]:
            quantizedAmplitude=midpointsList[i]
            currentLevel=i
            return quantizedAmplitude,currentLevel
        
    return quantizedAmplitude,currentLevel

def createRanges(numberOfLevels:int,min:float,max:float,delta:float):
    rangeList:list[tuple[float,float]]=[]
    midpointsList:list[float]=[]
    currentMin=min
    for i in range(numberOfLevels):
        currentMax=currentMin+delta
        if i==numberOfLevels-1:
            currentMax=max
        pair=(currentMin, currentMax)
        rangeList.append(pair)
        midpoint=(currentMin+currentMax)/2
        midpointsList.append(midpoint)
        currentMin=currentMax

    return rangeList, midpointsList

def quantizeSignalByLevels(signal:SignalData, numberOfLevels:int, write:bool=True):
    global signalCounter
    numberOfBits:int=int(math.log2(numberOfLevels))
    resultantSignal=quantizeSignalByBits(signal,numberOfBits,write=False)
    if write:
        writeSignal(resultantSignal,signalCounter,WriteMethod.quantizedLevels,numberOfBits)
        signalCounter+=1
    
    return resultantSignal

def DFT(signal:SignalData,write:bool=True, plot:bool=True):
    global signalCounter
    
    resultantSignal:SignalData = SignalData()
    resultantSignal.SignalType = not signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic
    resultantSignal.N1 = signal.N1
    
    frequencies = signal.data.keys()
    length:int = signal.N1
    
    for k in frequencies:
        amplitude:complex=0
        for n in frequencies:
            amplitude += signal.data[n] * math.e**((-1j*2*math.pi*k*n)/length)

        phaseValue:float = phase(amplitude)
        realAmplitude:float = math.sqrt(amplitude.real**2+amplitude.imag**2)
        resultantSignal.data[k] = (realAmplitude, phaseValue)
    
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1

    if plot:
        discreteRepresentation(resultantSignal)
    
    return resultantSignal