from tkinter import *
from enum import Enum
from buttonFunctions import *
from signalReader import *
import math
from QuantizedSignal import *
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
    global signalCounter
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType = signalList[0].SignalType
    resultantSignal.IsPeriodic = all(signal.IsPeriodic for signal in signalList)
    for i in range(max(signalList,key=lambda signal:signal.N1).N1):
        res:float=0
        for signal in signalList:
            res+=signal.data[i]
        resultantSignal.data[i]=res
    writeSignal(resultantSignal,signalCounter)
    signalCounter+=1
    signalList=[]

def subtractSignals():
    global signalList
    global signalCounter
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
    writeSignal(resultantSignal,signalCounter)
    signalCounter+=1
    signalList=[]


def multiplySignal(signal:SignalData,constant:float):
    global signalCounter
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1
    for index in signal.data.keys():
        resultantSignal.data[index]=signal.data[index]*constant
    writeSignal(resultantSignal,signalCounter)
    signalCounter+=1

def squareSignal(signal:SignalData):
    global signalCounter
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1
    for index in signal.data.keys():
        resultantSignal.data[index]=signal.data[index]*signal.data[index]
    writeSignal(resultantSignal,signalCounter)
    signalCounter+=1

def accumulateSignal(signal:SignalData):
    global signalCounter
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1
    resSum:float=0
    for index in signal.data.keys():
        resSum+=signal.data[index]
        resultantSignal.data[index]=resSum
    writeSignal(resultantSignal,signalCounter)
    signalCounter+=1


def calculate(mode:operation):
    match mode:
        case operation.addition:
            addSignals()
        case operation.subtraction:
            subtractSignals()

def normalizeMinMax(signal:SignalData):
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
    
    writeSignal(resultantSignal,signalCounter)
    signalCounter+=1

def normalizePeak(signal:SignalData):
    global signalCounter
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1
    maxValue:float=abs(max(signal.data.values()))

    for index in signal.data.keys():
        resultantSignal.data[index]=signal.data[index]/maxValue
    
    writeSignal(resultantSignal,signalCounter)
    signalCounter+=1


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
        resultantSignal.data.append((currentLevel, quantizedAmplitude))
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

def quantizeSignalByLevels(signal:SignalData, numberOfLevels:int):
    numberOfBits:int=math.log2(numberOfLevels)
    resultantSignal=quantizeSignalByBits(signal,numberOfBits,write=False)
    writeSignal(resultantSignal,signalCounter,WriteMethod.quantizedLevels,numberOfBits)