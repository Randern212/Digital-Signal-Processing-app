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

frequencyMenu:Menu=Menu(menuBar,tearoff=0)

menuBar.add_cascade(label="Frequency Domain",menu=frequencyMenu)
frequencyMenu.add_command(label="Fourier Transform", command=lambda:createFourierWindow(False))
frequencyMenu.add_command(label="FFT", command=lambda:createFourierWindow(True))
frequencyMenu.add_command(label="Display Dominant Frequencies", command=createDisplayDomFreqWindow)
frequencyMenu.add_command(label="Modify the Amplitude",command=lambda:createModificationWindow(modificationTarget.amp))
frequencyMenu.add_command(label="Modify the Phase",command=lambda:createModificationWindow(modificationTarget.phase))
frequencyMenu.add_command(label="Remove a DC component",command=createDCRemovalWindow)
frequencyMenu.add_command(label="Remove a DC component using DFT",command=lambda:createDCRemovalWindow(True))
frequencyMenu.add_command(label="IDFT Reconstruction",command=lambda:createIDFTReconstructionWindow(False))
frequencyMenu.add_command(label="IFFT",command=lambda:createIDFTReconstructionWindow(True))

timeMenu:Menu=Menu(menuBar,tearoff=0)

menuBar.add_cascade(label="Time Domain",menu=timeMenu)
timeMenu.add_command(label="Smoothing",command=createSmoothingWindow)
timeMenu.add_command(label="Sharpening",command=createSharpeningWindow)
timeMenu.add_command(label="Delaying/Advancing",command=createDelayingWindow)
timeMenu.add_command(label="Folding",command=createFoldingWindow)
timeMenu.add_command(label="Convolution",command=createConvolutionWindow)
timeMenu.add_command(label="Correlation",command=createCorrelationWindow)
timeMenu.add_command(label="Autocorrelation",command=createAutocorrelationWindow)
timeMenu.add_command(label="Periodic Correlation",command=createPeriodicCorrelationWindow)
timeMenu.add_command(label="FIR Filtering",command=createFIRwindow())

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
                                   command=lambda:createQuantizationWindow(quantizationType.bits),
                                   text="Quantize a signal by bits",
                                   font=("times new roman", 8))

quantizeSignalButtonByLevels:Button=Button(mainWindow,
                                   command=lambda:createQuantizationWindow(quantizationType.levels),
                                   text="Quantize a signal by levels",
                                   font=("times new roman", 8))
#=============================================================================

pickSignal.pack()
targetedSignalEntry.pack()
discreteSignalButton.pack()
ContinousSignalButton.pack()
quantizeSignalButtonByBits.pack()
quantizeSignalButtonByLevels.pack()