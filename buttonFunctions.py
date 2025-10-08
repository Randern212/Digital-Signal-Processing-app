from tkinter import *
from tkinter import filedialog
from signalReader import *
from signalClass import *
from plotFunctions import *

filePath:str = ""
targetSignals:dict={}
signalCounter:int=0

def submitFile(window:Tk):
    global filePath
    global targetSignals
    global signalCounter

    filePath = filedialog.askopenfilename(title="pick a signal file",
                                           filetypes=(("text files","*.txt"),("all files","*.*")))
    targetSignals[signalCounter]=readSignal(filePath=filePath)
    
    discreteSignalButton:Button=Button(window,
                               command=lambda:discreteRepresentation(targetSignals[signalCounter]),
                               text="Discrete Signal"+str(signalCounter),
                                font=("times new roman", 8))
    discreteSignalButton.pack()

    ContinousSignalButton:Button=Button(window,
                               command=lambda:continousRepresentation(targetSignals[signalCounter]),
                               text="Continous Signal"+str(signalCounter),
                                font=("times new roman", 8))
    ContinousSignalButton.pack()
    signalCounter+=1