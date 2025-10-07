from tkinter import filedialog
from signalReader import *
from signalClass import *

filePath:str = ""
targetSignal:SignalData=None

def submitFile():
    global filePath
    global targetSignal
    filePath = filedialog.askopenfilename(title="pick a signal file" , filetypes=(("text files","*.txt"),("all files","*.*")))
    targetSignal=readSignal(filePath=filePath)
