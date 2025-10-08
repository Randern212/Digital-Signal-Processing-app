from tkinter import *
import buttonFunctions as btf

mainWindow = Tk()
mainWindow.geometry("800x800")
mainWindow.title("Digital Signal Processing Application by Randern212")
mainWindow.config(background="#2a3f5e")

pickSignal:Button=Button(mainWindow,
                          command=lambda: btf.submitFile(mainWindow),
                          text="Choose signal file",
                            font=("times new roman", 12))

pickSignal.pack()