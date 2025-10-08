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
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType = signalList[0].SignalType
    resultantSignal.IsPeriodic = all(signal.IsPeriodic for signal in signalList)
    for i in range(max(signalList,key=lambda signal:signal.N1).N1):
        res:float=0
        for signal in signalList:
            res+=signal.data[i]
        resultantSignal.data[i]=res

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

def multiplySignal(signal:SignalData,constant:float):
    resultantSignal:SignalData=SignalData()
    resultantSignal.SignalType=signal.SignalType
    resultantSignal.IsPeriodic=signal.IsPeriodic
    resultantSignal.N1=signal.N1
    for index in signal.data.keys():
        resultantSignal.data[index]=signal.data[index]*constant

def calculate(mode:operation):
    match mode:
        case operation.addition:
            addSignals()
        case operation.subtraction:
            subtractSignals()

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
    multiplicationWindow=Toplevel()
    constantEntry:Entry=Entry(multiplicationWindow)
    signalEntry:Entry=Entry(multiplicationWindow)
    multiplyButton:Button=Button(multiplicationWindow,text="multiply",command=lambda:multiplySignal(targetSignals[int(signalEntry.get(),constantEntry.get())]))

    constantEntry.pack()
    signalEntry.pack()
    multiplyButton.pack()