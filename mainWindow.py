from tkinter import *
import buttonFunctions as btf
from plotFunctions import *

mainWindow = Tk()
mainWindow.geometry("420x420")
mainWindow.title("Digital Signal Processing Application by Randern212")
mainWindow.config(background="#2a3f5e")

pickSignal:Button=Button(mainWindow,
                          command= btf.submitFile,
                          text="Choose signal file",
                            font=("times new roman", 12))

targetedSignalEntry:Entry=Entry(mainWindow)

discreteSignalButton:Button=Button(mainWindow,
                                    command=lambda:discreteRepresentation(btf.targetSignals[int(targetedSignalEntry.get())]),
                                    text="Discrete Display",
                                    font=("times new roman", 8))

ContinousSignalButton:Button=Button(mainWindow,
                                    command=lambda:continousRepresentation(btf.targetSignals[int(targetedSignalEntry.get())]),
                                    text="Continous Display",
                                    font=("times new roman", 8))

targetedSignalEntry.pack()
discreteSignalButton.pack()
ContinousSignalButton.pack()
pickSignal.pack()