from tkinter import *
from enum import Enum
from buttonFunctions import *
from signalReader import *

signalList:list[SignalData]=[]

class operation(Enum):
    addition=0
    subtraction=1
    multiplication=2

def addSignals():
    global signalList
    resultantSignal:SignalData=SignalData()
    for i in max(signalList,key=lambda signal:signal.N1):
        sum:float=0
        for signal in signalList:
            sum+=signal.data[i]
        resultantSignal.data[i]=sum

def subtractSignals():
    pass

def multiplySignals():
    pass

def calculate(mode:operation):
    match mode:
        case operation.addition:
            addSignals()
        case operation.subtraction:
            subtractSignals()
        case operation.multiplication:
            multiplySignals()

def createOperationWindow(mode:operation):
    global signalList
    operationWindow:Toplevel=Toplevel()
    chosenSignal:Entry = Entry(operationWindow).pack()
    pushButton:Button=Button(operationWindow,text="push signal",command=lambda:signalList.append(targetSignals[int(chosenSignal.get())]))
    calculateButton:Button=Button(operationWindow,text="Calculate",command=lambda:calculate(mode)).pack()