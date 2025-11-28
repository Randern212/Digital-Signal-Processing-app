from tkinter import *
from enum import Enum
from buttonFunctions import *
from signalReader import *
import math
from QuantizedSignal import *
from plotFunctions import *
from cmath import *

from CompareSignals import*
from signalcompare import*

class operation(Enum):
    addition=0
    subtraction=1

class signalType(Enum):
    sin=0
    cosine=1

class quantizationType(Enum):
    bits=0
    levels=1

class modificationTarget(Enum):
    amp=0
    phase=1

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

def displayDomFrequency(signal:SignalData,write:bool=True):
    global signalCounter

    normalizedSignal:SignalData=normalizePeak(signal)
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType = signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic

    for i in range(normalizedSignal.N1):
        if normalizedSignal.SignalType==1:
            normalizedAmplitude=normalizedSignal.data[i][0]
        else:
            normalizedAmplitude=normalizedSignal.data[i]
        
        if normalizedAmplitude>0.5:
            resultantSignal.data[i]=normalizedAmplitude

    resultantSignal.N1=len(resultantSignal.data)

    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
    
    return readSignal

def removeDcComponentUsingDFT(signal:SignalData, write:bool=True):
    global signalCounter
    
    resultantSignal:SignalData = SignalData()
    frequencyDomainSignal=DFT(signal,4000,False,False)
    frequencyDomainSignal.data[0]=(0,0)
    resultantSignal=IDFT(frequencyDomainSignal,True)
    
    testIndices=[]
    testSamples=[]

    for i in range(resultantSignal.N1):
        testIndices.append(i)
        testSamples.append(resultantSignal.data[i])

    SignalsAreEqual("DC removal","tests\DC\DC_component_output.txt",testIndices,testSamples)

    return resultantSignal

def removeDcComponent(signal:SignalData, write:bool=True):
    global signalCounter
    
    resultantSignal:SignalData = SignalData()
    resultantSignal.SignalType = signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic
    resultantSignal.N1 = signal.N1

    meanDC = sum(signal.data.values()) / signal.N1
    
    for index, amplitude in signal.data.items():
        resultantAMP = amplitude - meanDC
        resultantSignal.data[index] = resultantAMP
    
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
    
    return resultantSignal

def DFT(signal:SignalData,samplingFrequency:float,write:bool=True, plot:bool=True):
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
        step:float=(2*math.pi)/length*(1/1000*samplingFrequency)
        discreteRepresentation(resultantSignal,step)
    
    return resultantSignal

def FFT(signal:SignalData,samplingFrequency:float,write:bool=True, plot:bool=True):
    global signalCounter
    
    resultantSignal:SignalData = SignalData()
    resultantSignal.SignalType = not signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic
    resultantSignal.N1 = signal.N1

    testAmplitudes=[]
    testPhases=[]

    amplitudes=recurseFFT(signal.data)
    for i in range(resultantSignal.N1):
        phaseValue:float = phase(amplitudes[i])
        realAmplitude:float = math.sqrt(amplitudes[i].real**2+amplitudes[i].imag**2)
        resultantSignal.data[i] = (realAmplitude, phaseValue)
        testAmplitudes.append(realAmplitude)
        testPhases.append(phaseValue)

    #Testing=========================================================================
    expectedAmp=[]
    expectedPhase=[]
    expectedOutput=readSignal("tests\Fourier\IDFTinput.txt",True)
    for a,p in expectedOutput.data.values():
        expectedAmp.append(a)
        expectedPhase.append(p)
    
    if SignalComapreAmplitude(expectedAmp,testAmplitudes) and SignalComaprePhaseShift(expectedPhase,testPhases):
        print("====================================================PASSED================================================================")
    else:
        print("------------------------------------------Failed--------------------------------------------------")
    #================================================================================


    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1

    if plot:
        step:float=(2*math.pi)/resultantSignal.N1*(1/1000*samplingFrequency)
        discreteRepresentation(resultantSignal,step)
    


    return resultantSignal


def recurseFFT(X,inverse:bool=False):
    length=len(X)
    Wfunction=None

    if inverse:
        Wfunction=caclculateOmegaFactorInverse
    else:
        Wfunction=calculateOmegaFactor

    if length==2:
        return [X[0]+X[1],X[0]-X[1]]
    else:
        evenL:list=[]
        oddL:list=[]
        for i in range(length):
            if i%2==0:
                evenL.append(X[i])
            else:
                oddL.append(X[i])

        fft1=recurseFFT(evenL,inverse)
        fft2=recurseFFT(oddL,inverse)
        resultantData:list=[0]*length

        for k in range(int(length/2)):
            w=Wfunction(k, length)
            resultantData[k]=butterflyTop(fft1[k],fft2[k],w)
            resultantData[int(k+(length/2))]=butterflyDown(fft1[k],fft2[k],w)
        return resultantData
    
def butterflyTop(fft1, fft2, W):
    return fft1 + W * fft2

def butterflyDown(fft1, fft2, W):
    return fft1 - W * fft2

def calculateOmegaFactor(k,N):
    return exp((-1j*2*pi*k)/N)

def caclculateOmegaFactorInverse(k,N):
    return exp((1j*2*pi*k)/N)

def IFFT(signal:SignalData,write:bool=True,):
    global signalCounter

    resultantSignal:SignalData = SignalData()
    resultantSignal.SignalType = not signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic
    length = resultantSignal.N1 = signal.N1
    
    complexValues=[]
    for n in range(length):
        amplitude, phase = signal.data[n]
        complexValues.append(amplitude * exp(1j * phase))
    
    timeDomainResult=recurseFFT(complexValues,True)

    testAmplitude=[]
    for i in range(length):
        resultantSignal.data[i]=round(timeDomainResult[i].real/length)
        testAmplitude.append(round(timeDomainResult[i].real/length))

    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1

    #Testing=========================================================================
    expectedAmplitudes=[]
    expectedOutput=readSignal("tests\Fourier\Output_Signal_IDFT.txt")
    for amp in expectedOutput.data.values():
        expectedAmplitudes.append(amp)
    if (SignalComapreAmplitude(expectedAmplitudes,testAmplitude)):
        print("====================================================PASSED================================================================")
    else:
        print("------------------------------------------Failed--------------------------------------------------")
    #================================================================================

    return resultantSignal

def IDFT(signal:SignalData,write:bool=True):
    global signalCounter

    resultantSignal:SignalData = SignalData()
    resultantSignal.SignalType = not signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic
    length = resultantSignal.N1 = signal.N1
    
    for n in range(length):
        term:complex=complex(0,0)
        for k in range(length):
            amplitude, phase = signal.data[k]
            complexValue = amplitude * exp(1j * phase)
            term+=complexValue * math.e ** ((1j * 2 * math.pi * n * k)/length)
        resultantSignal.data[n]=term.real/length

    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
    
    return resultantSignal

def modifyValue(signal:SignalData,dataIndex:int,dataValue:float,mode:modificationTarget):
    oldAmplitude,oldPhase=signal.data[dataIndex]
    if mode==modificationTarget.amp:
        signal.data[dataIndex]=(dataValue,oldPhase)
    else:
        signal.data[dataIndex]=(oldAmplitude,dataValue)
      