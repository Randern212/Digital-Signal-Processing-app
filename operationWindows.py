
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


def createDCRemovalWindow(useDFT:bool=False):
    method:callable=NONE
    if useDFT:
        method=removeDcComponentUsingDFT
    else:
        method=removeDcComponent
    
    DCremoverWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(DCremoverWindow)
    DCremoverButton:Button=Button(DCremoverWindow,text="Remove DC component",command=lambda:method(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    DCremoverButton.pack()

def createIDFTReconstructionWindow(performFFT:bool):
    FTmethod:callable=NONE
    if performFFT:
        FTmethod=IFFT
    else:
        FTmethod=IDFT
    
    reconstructionWindow:Toplevel=Toplevel()

    pickSignal:Button=Button(reconstructionWindow,
                          command= lambda:submitFile(True),
                          text="Choose signal file to",
                            font=("times new roman", 12))
    signalEntry:Entry=Entry(reconstructionWindow)
    reconstructionButton:Button=Button(reconstructionWindow,text="Perform IDFT",command=lambda:FTmethod(targetSignals[int(signalEntry.get())]))
    
    pickSignal.pack()
    signalEntry.pack()
    reconstructionButton.pack()

def createSmoothingWindow():
    smoothingWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(smoothingWindow)
    sizeEntry:Entry=Entry(smoothingWindow)
    smoothingButton:Button=Button(smoothingWindow,text="Smooth",command=lambda:smoothSignal(targetSignals[int(signalEntry.get())],int(sizeEntry.get())))

    signalEntry.pack()
    sizeEntry.pack()
    smoothingButton.pack()
    
def createSharpeningWindow():
    sharpeningWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(sharpeningWindow)
    sharpening1Button:Button=Button(sharpeningWindow,text="Sharpen 1st",command=lambda:sharpenSignal1st(targetSignals[int(signalEntry.get())]))
    sharpening2Button:Button=Button(sharpeningWindow,text="Sharpen 2nd",command=lambda:sharpenSignal2nd(targetSignals[int(signalEntry.get())]))
    sharpeningButton:Button=Button(sharpeningWindow,text="Sharpen both",command=lambda:sharpenSignal(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    sharpening1Button.pack()
    sharpening2Button.pack()
    sharpeningButton.pack()


def createDelayingWindow():
    delayingWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(delayingWindow)
    KEntry:Entry=Entry(delayingWindow)
    delayingButton:Button=Button(delayingWindow,text="delay",command=lambda:delayAdvanceSignal(targetSignals[int(signalEntry.get())],int(KEntry.get())))

    signalEntry.pack()
    KEntry.pack()
    delayingButton.pack()

def createFoldingWindow():
    foldingWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(foldingWindow)
    foldingButton:Button=Button(foldingWindow,text="fold",command=lambda:foldSignal(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    foldingButton.pack()

def createConvolutionWindow():
    convolutionWindow:Toplevel=Toplevel()
    signalEntry1:Entry=Entry(convolutionWindow)
    signalEntry2:Entry=Entry(convolutionWindow)

    convolutionButton:Button=Button(convolutionWindow,text="Convolve",command=lambda:convolve(targetSignals[int(signalEntry1.get())],targetSignals[int(signalEntry2.get())]))

    signalEntry1.pack()
    signalEntry2.pack()

    convolutionButton.pack()

def createCorrelationWindow():
    correlationWindow:Toplevel=Toplevel()
    signalEntry1:Entry=Entry(correlationWindow)
    signalEntry2:Entry=Entry(correlationWindow)

    correlationButton:Button=Button(correlationWindow,text="Correlate",command=lambda:correlate(targetSignals[int(signalEntry1.get())],targetSignals[int(signalEntry2.get())]))

    signalEntry1.pack()
    signalEntry2.pack()

    correlationButton.pack()

def createAutocorrelationWindow():
    autocorrelationWindow:Toplevel=Toplevel()
    signalEntry:Entry=Entry(autocorrelationWindow)
    autocorrelateButton:Button=Button(autocorrelationWindow,text="auto correlate",command=lambda:autocorrelate(targetSignals[int(signalEntry.get())]))

    signalEntry.pack()
    autocorrelateButton.pack()

def createPeriodicCorrelationWindow():
    correlationWindow:Toplevel=Toplevel()
    signalEntry1:Entry=Entry(correlationWindow)
    signalEntry2:Entry=Entry(correlationWindow)

    correlationButton:Button=Button(correlationWindow,text="Correlate",command=lambda:periodicCorrelate(targetSignals[int(signalEntry1.get())],targetSignals[int(signalEntry2.get())]))

    signalEntry1.pack()
    signalEntry2.pack()

    correlationButton.pack()

def createFIRwindow():
    FIRwindow = Toplevel()
    signalEntry = Entry(FIRwindow)
    testEntry = Entry(FIRwindow)

    pickedFilter = None
    
    def handleSubmitFilter():
        nonlocal pickedFilter  
        pickedFilter = submitFilter() 
        return pickedFilter
    
    def handleCreateFilterSignal():
        nonlocal pickedFilter
        if pickedFilter is not None:
            createFilterSignal(pickedFilter,int(testEntry.get()))
    
    pickFilter = Button(
        FIRwindow,
        command=handleSubmitFilter,
        text="Choose filter file",
        font=("times new roman", 12)
    )
    
    filterButton = Button(
        FIRwindow,
        text="Apply Filter",
        command=lambda: applyFilter(targetSignals[int(signalEntry.get())],pickedFilter,int(testEntry.get()))
    )
    
    filterSignalButton = Button(
        FIRwindow,
        text="Just Create Filter Signal",
        command=handleCreateFilterSignal
    )
    
    pickFilter.pack()
    signalEntry.pack()
    testEntry.pack()
    filterSignalButton.pack()
    filterButton.pack()

def createSamplingWindow():
    FIRwindow = Toplevel()
    signalEntry = Entry(FIRwindow)
    # testEntry = Entry(FIRwindow)
    entryL=Entry(FIRwindow)
    entryM=Entry(FIRwindow)

    pickedFilter = None
    
    def handleSubmitFilter():
        nonlocal pickedFilter  
        pickedFilter = submitFilter() 
        return pickedFilter
    
    pickFilter = Button(
        FIRwindow,
        command=handleSubmitFilter,
        text="Choose filter file",
        font=("times new roman", 12)
    )
    
    filterButton = Button(
        FIRwindow,
        text="Apply Filter",
        command=lambda: sample(targetSignals[int(signalEntry.get())],pickedFilter,int(entryM.get()),int(entryL.get()))
    )
    

    
    pickFilter.pack()
    signalEntry.pack()
    entryL.pack()
    entryM.pack()
    # testEntry.pack()
    filterButton.pack()