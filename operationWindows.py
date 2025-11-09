
from operations import * 
import math
signalList:list[SignalData]=[]


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
    multiplicationWindow:Toplevel=Toplevel()
    constantEntry:Entry=Entry(multiplicationWindow)
    signalEntry:Entry=Entry(multiplicationWindow)
    multiplyButton:Button=Button(multiplicationWindow,text="multiply",command=lambda:multiplySignal(targetSignals[int(signalEntry.get())],float(constantEntry.get())))

    constantEntry.pack()
    signalEntry.pack()
    multiplyButton.pack()

def createSquaringWindow():
    squaringWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(squaringWindow)
    squaringButton:Button=Button(squaringWindow,text="Square Signal",command=lambda:squareSignal(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    squaringButton.pack()

def createAccumulationWindow():
    accumulationWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(accumulationWindow)
    accumulationButton:Button=Button(accumulationWindow,text="Square Signal",command=lambda:accumulateSignal(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    accumulationButton.pack()

def createNormalizationWindow():
    normalizationWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(normalizationWindow)
    minMaxButton:Button=Button(normalizationWindow,text="normalize [0,1]",command=lambda:normalizeMinMax(targetSignals[int(signalEntry.get())]))
    peakButton:Button=Button(normalizationWindow,text="normalize [-1,1]",command=lambda:normalizePeak(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    minMaxButton.pack()
    peakButton.pack()

def createGenerationWindow(mode:signalType):
    generationWinow:Toplevel=Toplevel()
    amplitudeEntry:Entry=Entry(generationWinow)
    phaseShiftEntry:Entry=Entry(generationWinow)
    analogFrequencyEntry:Entry=Entry(generationWinow)
    samplingFrequencyEntry:Entry=Entry(generationWinow)
    trigFunction:callable=math.sin
    match mode:
        case signalType.sin:
            trigFunction=math.sin
        case signalType.cosine:
            trigFunction=math.cos
    generationButton:Button=Button(generationWinow,text="Generate Signal",
                                    command=lambda:generateSignal(float(amplitudeEntry.get()),float(phaseShiftEntry.get()),float(analogFrequencyEntry.get()),float(samplingFrequencyEntry.get()),trigFunction))
    
    amplitudeEntry.pack()
    phaseShiftEntry.pack()
    analogFrequencyEntry.pack()
    samplingFrequencyEntry.pack()
    generationButton.pack()

def createQuantizationWindow(mode:quantizationType):
    chosenMethod:callable=None
    
    if mode==quantizationType.bits:
        chosenMethod=quantizeSignalByBits
    else:
        chosenMethod=quantizeSignalByLevels
    
    quantizationWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(quantizationWindow)
    bitsOrLevelsEntry:Entry=Entry(quantizationWindow)
    quantizeButton:Button=Button(quantizationWindow,text="Quantize", command=lambda:chosenMethod(targetSignals[int(signalEntry.get())],int(bitsOrLevelsEntry.get())))
    
    signalEntry.pack()
    bitsOrLevelsEntry.pack()
    quantizeButton.pack()

def createFourierWindow(performFFT:bool):
    FTmethod:callable=NONE
    if performFFT:
        FTmethod=FFT
    else:
        FTmethod=DFT
    fourierWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(fourierWindow)
    samplingFrequencyEntry:Entry=Entry(fourierWindow)
    transformButton:Button=Button(fourierWindow,text="Transform",command=lambda:FTmethod(targetSignals[int(signalEntry.get())],float(samplingFrequencyEntry.get())))

    signalEntry.pack()
    samplingFrequencyEntry.pack()
    transformButton.pack()

def createDisplayDomFreqWindow():
    domFrequencyWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(domFrequencyWindow)
    domFrequencyButton:Button=Button(domFrequencyWindow,text="View Dominant Frequencies",command=lambda:displayDomFrequency(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    domFrequencyButton.pack()


def createModificationWindow(mode:modificationTarget):
    modificationWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(modificationWindow)
    indexEntry:Entry=Entry(modificationWindow)
    dataEntry:Entry=Entry(modificationWindow)

    modificationButton:Button=Button(modificationWindow,text="Modify data",command=lambda:modifyValue(targetSignals[int(signalEntry.get())],int(indexEntry.get()),float(dataEntry.get()),mode))

    signalEntry.pack()
    indexEntry.pack()
    dataEntry.pack()
    modificationButton.pack()


def createDCRemovalWindow():
    DCremoverWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(DCremoverWindow)
    DCremoverButton:Button=Button(DCremoverWindow,text="Remove DC component",command=lambda:removeDcComponent(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    DCremoverButton.pack()

def createIDFTReconstructionWindow():
    reconstructionWindow:Toplevel=Toplevel()

    pickSignal:Button=Button(reconstructionWindow,
                          command= lambda:submitFile(True),
                          text="Choose signal file to",
                            font=("times new roman", 12))
    signalEntry:Entry=Entry(reconstructionWindow)
    reconstructionButton:Button=Button(reconstructionWindow,text="Perform IDFT",command=lambda:IDFT(targetSignals[int(signalEntry.get())]))
    
    pickSignal.pack()
    signalEntry.pack()
    reconstructionButton.pack()