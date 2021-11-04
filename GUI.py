#!/usr/bin/python3

#import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image

def runDTC():
	os.system('./DTCParse.py')

#Create the Window
window = Tk()

window.title("OBD-II Reader")

#Window size
#window.geometry("500x500")

#Tab Creation and Labeling
tabs = ttk.Notebook(window)
tabDTC = ttk.Frame(tabs)
tabFFD = ttk.Frame(tabs)
tabRTD = ttk.Frame(tabs)
tabSET = ttk.Frame(tabs)

tabs.add(tabDTC, text="DTC")
tabs.add(tabFFD, text="FFD")
tabs.add(tabRTD, text="RTD")
tabs.add(tabSET, text="SET")

lblDTC = ttk.Label(tabDTC, text= 'label1')
lblDTC.grid(column=0, row=0)

lblFFD = ttk.Label(tabFFD, text= 'label2')
lblFFD.grid(column=0, row=0)

img = ImageTk.PhotoImage( Image.open("Engine_coolant_temperature.png"))
labelTEST = ttk.Label(tabFFD, image = img,  text= "Test")
labelTEST.image = img
labelTEST.grid(column=0, row=1)

lblRTD = ttk.Label(tabRTD, text= 'label3')
lblRTD.grid(column=0, row=0)

lblSET = ttk.Label(tabSET, text= 'label4')
lblSET.grid(column=0, row=0)

tabs.pack(expand=1, fill='both')

#Button on the SET tab that closes the GUI when pressed
quitButton = Button(tabSET, text="Quit", command=window.destroy)
quitButton.grid(column=5, row=5)

DTCButton = Button(tabDTC, text="Look For Trouble Codes", command=runDTC)
DTCButton.grid(column=0, row = 1)
#DTCButton.pack()
window.mainloop()


