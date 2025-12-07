from tkinter import filedialog
from signalReader import *
from signalClass import *
from filterClass import *

targetSignals:dict={}
signalCounter:int=0
LoadedFilter:Filter

def submitFile(skipFrequency:bool=False):
    global targetSignals
    global signalCounter

    filePath = filedialog.askopenfilename(title="pick a signal file",
                                           filetypes=(("text files","*.txt"),("all files","*.*")))
    targetSignals[signalCounter]=readSignal(filePath=filePath, skipFrequency=skipFrequency)
    signalCounter+=1

def submitFilter():
    global LoadedFilter
    filePath = filedialog.askopenfilename(title="pick a signal file",
                                           filetypes=(("text files","*.txt"),("all files","*.*")))
    
    LoadedFilter = readFilter(filePath) 