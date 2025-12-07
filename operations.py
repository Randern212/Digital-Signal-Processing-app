from tkinter import *
from enum import Enum
from buttonFunctions import *
from signalReader import *
import math
from QuantizedSignal import *
from plotFunctions import *
from cmath import *
from collections import deque
from typing import Final

#TESTING MODULES=====================================================================
from ConvTest import *
from CompareSignals import*
from signalcompare import*
from CompareSignal import*
from Shift_Fold_Signal import*
from DerivativeSignal import*
#====================================================================================
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

testFIR={
    1:"tests\FIR test cases\Testcase 1\LPFCoefficients.txt",
    2:"tests\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt",
    3:"tests\FIR test cases\Testcase 3\HPFCoefficients.txt",
    4:"tests\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt",
    5:"tests\FIR test cases\Testcase 5\BPFCoefficients.txt",
    6:"tests\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt",
    7:"tests\FIR test cases\Testcase 7\BSFCoefficients.txt",
    8:"tests\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt"
}

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


def smoothSignal(signal:SignalData,windowSize:int,write:bool=True):
    global signalCounter

    resultantSignal = SignalData()
    resultantSignal.SignalType = signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic
    resultantSignal.N1 = signal.N1 - (windowSize - 1)
        
    indices = sorted(signal.data.keys())
    values = [signal.data[i] for i in indices]
        
    for i in range(resultantSignal.N1):
        windowSum = sum(values[i:i + windowSize])
        avg = windowSum / windowSize
        resultantSignal.data[indices[i]] = avg

    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
        Compare_Signals("tests\Moving Average\OutMovAvgTest1.txt",list(resultantSignal.data.keys()),list(resultantSignal.data.values()))
        Compare_Signals("tests\Moving Average\OutMovAvgTest2.txt",list(resultantSignal.data.keys()),list(resultantSignal.data.values()))
    return resultantSignal

def sharpenSignal(signal:SignalData,write:bool=True):
    derv1st=sharpenSignal1st(signal,write)
    derv2nd=sharpenSignal2nd(signal,write)
    DerivativeSignal(list(derv1st.data.values()),list(derv2nd.data.values()))

def sharpenSignal1st(signal:SignalData,write:bool=True):
    global signalCounter

    resultantSignal = SignalData()
    resultantSignal.SignalType = signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic
        
    indices = sorted(signal.data.keys())
    resultantSignal.N1 = len(indices) - 1
        
    for i in range(1, len(indices)):
        currentIndex = indices[i]
        previousIndex = indices[i-1]
        derivative = signal.data[currentIndex] - signal.data[previousIndex]
        resultantSignal.data[currentIndex] = derivative
        
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1

    return resultantSignal

def sharpenSignal2nd(signal:SignalData,write:bool=True):
    global signalCounter

    resultantSignal = SignalData()
    resultantSignal.SignalType = signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic
        
    indices = sorted(signal.data.keys())
    resultantSignal.N1 = len(indices) - 2
        
    for i in range(1, len(indices) - 1):
        currentIndex = indices[i]
        nextIndex = indices[i+1]
        previousIndex = indices[i-1]
        derivative = (signal.data[nextIndex] - 2 * signal.data[currentIndex] + signal.data[previousIndex])
        resultantSignal.data[currentIndex] = derivative
        
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
    
    return resultantSignal

def delayAdvanceSignal(signal:SignalData,k:int,write:bool=True):
    global signalCounter

    resultantSignal = SignalData()
    resultantSignal.SignalType = signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic
    resultantSignal.N1 = signal.N1
    k*=-1    
    for index, value in signal.data.items():
        resultantSignal.data[index - k] = value
        
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
        Shift_Fold_Signal("tests\Shifting and Folding\Output_ShifFoldedby500.txt",list(resultantSignal.data.keys()),list(resultantSignal.data.values()))
        Shift_Fold_Signal("tests\Shifting and Folding\Output_ShiftFoldedby-500.txt",list(resultantSignal.data.keys()),list(resultantSignal.data.values()))

    return resultantSignal

def foldSignal(signal:SignalData,write:bool=True):
    global signalCounter

    resultantSignal = SignalData()
    resultantSignal.SignalType = signal.SignalType
    resultantSignal.IsPeriodic = signal.IsPeriodic
    resultantSignal.N1 = signal.N1
        
    for index, value in signal.data.items():
            resultantSignal.data[-index] = value
        
    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
        Shift_Fold_Signal("tests\Shifting and Folding\Output_fold.txt",list(resultantSignal.data.keys()),list(resultantSignal.data.values()))

    return resultantSignal

def convolve(signal1:SignalData,signal2:SignalData,write:bool=True,test:bool=True):
    global signalCounter
    
    resultantSignal:SignalData = SignalData()
    resultantSignal.IsPeriodic=signal1.IsPeriodic or signal2.IsPeriodic
    resultantSignal.SignalType=0

    indices1 = sorted(signal1.data.keys())
    indices2 = sorted(signal2.data.keys())

    minIndex = min(indices1) + min(indices2)
    maxIndex = max(indices1) + max(indices2)
    
    resultantSignal.N1 = len(range(minIndex,maxIndex)) + 1

    for i in range(minIndex, maxIndex + 1):
        Yn=0
        for k in indices1:
            if (i-k) in signal2.data:
                Yn+=signal1.data[k] * signal2.data[i-k]
        resultantSignal.data[i]=Yn

    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
        if test:
            ConvTest(list(resultantSignal.data.keys()),list(resultantSignal.data.values()))
    
    return resultantSignal    

def correlate(signal1:SignalData,signal2:SignalData,write:bool=True):
    global signalCounter

    resultantSignal = SignalData()
    resultantSignal.SignalType = 0
    resultantSignal.IsPeriodic = 0
    resultantSignal.N1 = signal1.N1
    

    r:dict={}
    for j in range(resultantSignal.N1):
        rN = 0
        for n in range(signal1.N1):
            nj=(n+j)%signal1.N1
            rN+=(signal1.data[n]*signal2.data[nj])/resultantSignal.N1
        r[j]=rN


    calculatePCorrelation(resultantSignal,signal1,signal2,r)

    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
    
    Compare_Signals("tests\Point1 Correlation\CorrOutput.txt",list(resultantSignal.data.keys()),list(resultantSignal.data.values()))
    
    return resultantSignal

def autocorrelate(signal:SignalData,write:bool=True):
    return correlate(signal1=signal,signal2=signal,write=write)

def calculatePCorrelation(resultantSignal,signal1,signal2,r):
    sumOfSamples1=sum(x*x for x in list(signal1.data.values()))
    sumOfSamples2=sum(x*x for x in list(signal2.data.values()))
    
    denominator=(((sumOfSamples1*sumOfSamples2))**(1/2))/resultantSignal.N1
    for j in range(resultantSignal.N1):
        pN = r[j]/denominator
        resultantSignal.data[j] = pN

def periodicCorrelate(signal1:SignalData,signal2:SignalData,write:bool=True):
    global signalCounter

    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=0
    resultantSignal.IsPeriodic=1
    resultantSignal.N1=signal1.N1+signal2.N1-1

    samples1=list(signal1.data.values())
    samples2=list(signal2.data.values())
    r:dict={}

    if len(samples1) >= len(samples2):
        samplesFixed=samples1
        samplesToShift=samples2
    else:
        samplesFixed=samples2
        samplesToShift=samples1

    samplesFixed = (samplesFixed + [0] * resultantSignal.N1)[:resultantSignal.N1]
    samplesToShift = (samplesToShift + [0] * resultantSignal.N1)[:resultantSignal.N1]

    for n in range(resultantSignal.N1):
        r[n]=sum(a*b for a,b in zip(samplesFixed,samplesToShift))/resultantSignal.N1
        d = deque(samplesToShift)
        d.rotate(-1)
        samplesToShift = list(d)

    calculatePCorrelation(resultantSignal,signal1,signal2,r)

    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1

    Compare_Signals("tests\Correlation (different length)\CorrOutput.txt",list(resultantSignal.data.keys()),list(resultantSignal.data.values()))

    return resultantSignal

def applyFilter(signal:SignalData,LoadedFilter:Filter,testCase:int,write:bool=True):
    global signalCounter
    resultantSignal:SignalData= convolve(signal,createFilterSignal(LoadedFilter,False),write,False)
    fileName=testFIR[testCase]
    Compare_Signals(fileName,list(resultantSignal.data.keys()),list(resultantSignal.data.values()))
    return resultantSignal

rectangularAttenuation:Final = 21
hanningAttenuation:Final = 44
hammingAttenuation:Final = 53
blackmanAttenuation:Final = 74

rectangularTransitionWidth:Final = 0.9
hanningTransitionWidth:Final = 3.1
hammingTransitionWidth:Final = 3.3
blackmanTransitionWidth:Final = 5.5

def createFilterSignal(LoadedFilter:Filter,testCase:int,write:bool=True):
    global signalCounter

    windowFuntion:callable
    filterFunction:callable
    transitionWidth:float

    if LoadedFilter.stopBandAttenuation <= rectangularAttenuation:
        windowFuntion=rectangular
        transitionWidth=rectangularTransitionWidth
    elif LoadedFilter.stopBandAttenuation <= hanningAttenuation:
        windowFuntion=hanning
        transitionWidth=hanningTransitionWidth
    elif LoadedFilter.stopBandAttenuation <= hammingAttenuation:
        windowFuntion=hamming
        transitionWidth=hammingTransitionWidth
    else:
        windowFuntion=blackman
        transitionWidth=blackmanTransitionWidth
    
    windowLength = math.ceil(transitionWidth/(LoadedFilter.transitionBand/LoadedFilter.FS))
    
    if windowLength%2==0:
        windowLength+=1

    match LoadedFilter.filterType:
        case FilterType.LOW:
            LoadedFilter.FC+=(LoadedFilter.transitionBand/2)
            filterFunction=lowPassFiltering
        case FilterType.HIGH:
            LoadedFilter.FC-=(LoadedFilter.transitionBand/2)
            filterFunction=highPassFiltering
        case FilterType.BAND_PASS:
            LoadedFilter.F1-=(LoadedFilter.transitionBand/2)
            LoadedFilter.F2+=(LoadedFilter.transitionBand/2)
            filterFunction=bandPassFiltering
        case FilterType.BAND_STOP:
            LoadedFilter.F1+=(LoadedFilter.transitionBand/2)
            LoadedFilter.F2-=(LoadedFilter.transitionBand/2)
            filterFunction=bandStopFiltering

    LoadedFilter.FC/=LoadedFilter.FS
    LoadedFilter.F1/=LoadedFilter.FS
    LoadedFilter.F2/=LoadedFilter.FS

    wc=(2*pi*LoadedFilter.FC)
    w1=(2*pi*LoadedFilter.F1)
    w2=(2*pi*LoadedFilter.F2)
    
    windowRange=range(int(-(windowLength-1)/2), int((windowLength-1)/2)+1)

    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=0
    resultantSignal.IsPeriodic=0
    resultantSignal.N1=windowLength
    
    for n in windowRange:
        resultantSignal.data[n]=(filterFunction(n, LoadedFilter.FC, LoadedFilter.F1, LoadedFilter.F2, wc, w1, w2)*windowFuntion(n, windowLength)).real

    if write:
        writeSignal(resultantSignal,signalCounter)
        signalCounter+=1
        fileName=testFIR[testCase]
        Compare_Signals(fileName,list(resultantSignal.data.keys()),list(resultantSignal.data.values()))
    
    return resultantSignal

# Window Functions========================================
def rectangular(n,N):
    return 1

def hanning(n,N):
    return 0.5+(0.5*cos((2*pi*n)/N))

def hamming(n,N):
    return 0.54+(0.46*cos((2*pi*n)/N))

def blackman(n,N):
    return 0.42+(0.5*cos((2*pi*n)/(N-1)))+(0.08*cos((4*pi*n)/(N-1)))
# =========================================================

# Filter Functions========================================
def lowPassFiltering(n,fc,f1,f2,w,w1,w2):
    if n==0:
        return 2*fc
    return 2*fc*(sin(n*w)/(n*w))

def highPassFiltering(n,fc,f1,f2,w,w1,w2):
    if n==0:
        return 1 - (2*fc)
    return -2*fc*(sin(n*w)/(n*w))

def bandPassFiltering(n,fc,f1,f2,w,w1,w2):
    if n==0:
        return 2*(f2-f1)
    return (2*f2*(sin(n*w2)/(n*w2)))-(2*f1*(sin(n*w1)/(n*w1)))

def bandStopFiltering(n,fc,f1,f2,w,w1,w2):
    if n==0:
        return 1-(2*(f2-f1))
    return (2*f1*(sin(n*w1)/(n*w1)))-(2*f2*(sin(n*w2)/(n*w2)))
# =========================================================
