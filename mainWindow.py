from tkinter import *
from buttonFunctions import *
from plotFunctions import *
from operationWindows import*

mainWindow = Tk()
menuBar:Menu=Menu(mainWindow)
mainWindow.geometry("420x420")
mainWindow.title("Digital Signal Processing Application by Randern212")
mainWindow.config(background="#2a3f5e",menu=menuBar)

#Menus=========================================================================
arithmeticMenu:Menu=Menu(menuBar,tearoff=0)

menuBar.add_cascade(label="Arithmetic",menu=arithmeticMenu)
arithmeticMenu.add_command(label="Addition",command=lambda:createOperationWindow(operation.addition))
arithmeticMenu.add_command(label="Subtraction",command=lambda:createOperationWindow(operation.subtraction))
arithmeticMenu.add_command(label="Multiplication",command=createMultiplicationWindow)
arithmeticMenu.add_command(label="Squaring",command=createSquaringWindow)
arithmeticMenu.add_command(label="Normalization",command=createNormalizationWindow)
arithmeticMenu.add_command(label="Accumulation",command=createAccumulationWindow)

generationMenu:Menu=Menu(menuBar,tearoff=0)
menuBar.add_cascade(label="Generate",menu=generationMenu)
generationMenu.add_command(label="Sinusoidal",command=lambda:createGenerationWindow(signalType.sin))
generationMenu.add_command(label="Cosinusoidal",command=lambda:createGenerationWindow(signalType.cosine))
#==============================================================================

targetedSignalEntry:Entry=Entry(mainWindow)

#Buttons======================================================================
pickSignal:Button=Button(mainWindow,
                          command= submitFile,
                          text="Choose signal file",
                            font=("times new roman", 12))

discreteSignalButton:Button=Button(mainWindow,
                                    command=lambda:discreteRepresentation(targetSignals[int(targetedSignalEntry.get())]),
                                    text="Discrete Display",
                                    font=("times new roman", 8))

ContinousSignalButton:Button=Button(mainWindow,
                                    command=lambda:continousRepresentation(targetSignals[int(targetedSignalEntry.get())]),
                                    text="Continous Display",
                                    font=("times new roman", 8))

quantizeSignalButtonByBits:Button=Button(mainWindow,
                                   command=createQuantizationWindow,
                                   text="Quantize a signal by bits",
                                   font=("times new roman", 8))

quantizeSignalButtonByLevels:Button=Button(mainWindow,
                                   command=createQuantizationWindow,
                                   text="Quantize a signal by levels",
                                   font=("times new roman", 8))
#=============================================================================

pickSignal.pack()
targetedSignalEntry.pack()
discreteSignalButton.pack()
ContinousSignalButton.pack()
quantizeSignalButtonByBits.pack()
quantizeSignalButtonByLevels.pack()