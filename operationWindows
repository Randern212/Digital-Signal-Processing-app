from tkinter import *
from enum import Enum
from buttonFunctions import *

class operation(Enum):
    addition=0
    subtraction=1
    multiplication=2

def addSignals(signal1:SignalData,signal2:SignalData):
    pass

def subtractSignals(signal1:SignalData,signal2:SignalData):
    pass

def multiplySignals(signal1:SignalData,signal2:SignalData):
    pass

def calculate(mode:operation,id1:int,id2:int):
    signal1:SignalData=targetSignals[id1]
    signal2:SignalData=targetSignals[id2]
    match mode:
        case operation.addition:
            addSignals(signal1,signal2)
        case operation.subtraction:
            subtractSignals(signal1,signal2)
        case operation.multiplication:
            multiplySignals(signal1,signal2)

def createOperationWindow(mode:operation):
    operationWindow:Toplevel=Toplevel()
    field1:Entry = Entry(operationWindow).pack()
    field2:Entry =Entry(operationWindow).pack()
    calculateButton:Button=Button(operationWindow,text="Calculate",command=lambda:calculate(mode,int(field1.get()),int(field2.get()))).pack()