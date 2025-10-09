from tkinter import *
from enum import Enum
from buttonFunctions import *
from signalReader import *

signalList:list[SignalData]=[]

class operation(Enum):
    addition=0
    subtraction=1

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

    maxValue:float=max(signal.data.values())
    minValue:float=min(signal.data.values())
    
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

def createOperationWindow(mode:operation):
    global signalList
    operationWindow:Toplevel=Toplevel()
    chosenSignal:Entry = Entry(operationWindow)
    pushButton:Button=Button(operationWindow,text="push signal",command=lambda:signalList.append(targetSignals[int(chosenSignal.get())]))
    calculateButton:Button=Button(operationWindow,text="Calculate",command=lambda:calculate(mode))

    chosenSignal.pack()
    pushButton.pack()
    calculateButton.pack()

def createMultiplicationWindow():
    multiplicationWindow:Toplevel=Toplevel()
    constantEntry:Entry=Entry(multiplicationWindow)
    signalEntry:Entry=Entry(multiplicationWindow)
    multiplyButton:Button=Button(multiplicationWindow,text="multiply",command=lambda:multiplySignal(targetSignals[int(signalEntry.get())],float(constantEntry.get())))

    constantEntry.pack()
    signalEntry.pack()
    multiplyButton.pack()

def createSquaringWindow():
    squaringWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(squaringWindow)
    squaringButton:Button=Button(squaringWindow,text="Square Signal",command=lambda:squareSignal(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    squaringButton.pack()

def createAccumulationWindow():
    accumulationWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(accumulationWindow)
    accumulationButton:Button=Button(accumulationWindow,text="Square Signal",command=lambda:accumulateSignal(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    accumulationButton.pack()

def createNormalizationWindow():
    normalizationWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(normalizationWindow)
    minMaxButton:Button=Button(normalizationWindow,text="normalize [0,1]",command=lambda:normalizeMinMax(targetSignals[int(signalEntry.get())]))
    peakButton:Button=Button(normalizationWindow,text="normalize [-1,1]",command=lambda:normalizePeak(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    minMaxButton.pack()
    peakButton.pack()