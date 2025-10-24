from tkinter import filedialog
from signalReader import *
from signalClass import *

targetSignals:dict={}
signalCounter:int=0

def submitFile(skipFrequency:bool=False):
    global targetSignals
    global signalCounter

    filePath = filedialog.askopenfilename(title="pick a signal file",
                                           filetypes=(("text files","*.txt"),("all files","*.*")))
    targetSignals[signalCounter]=readSignal(filePath=filePath, skipFrequency=skipFrequency)
    signalCounter+=1