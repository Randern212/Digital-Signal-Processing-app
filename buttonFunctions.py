
from tkinter import *
from tkinter import filedialog

filePath:str = ""

def submitFile():
    global filePath
    filePath = filedialog.askopenfilename(title="pick a signal file" , filetypes=(("text files","*.txt"),("all files","*.*")))