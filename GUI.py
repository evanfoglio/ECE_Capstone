#!/usr/bin/python3

#import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image

def runDTC():
	os.system('./DTCParse.py')

def updateEngineSpeed():
	img = ImageTk.PhotoImage( Image.open("Engine_speed.png"))
	labelEngSpeed = ttk.Label(tabFFD2, image = img,  text= "Test")
	labelEngSpeed.image = img
	labelEngSpeed.grid(column=0, row=1)
	

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

tabFFD1 = ttk.Frame(tabs)
tabFFD2 = ttk.Frame(tabs)
tabFFD3 = ttk.Frame(tabs)
tabFFD4 = ttk.Frame(tabs)
tabFFD5 = ttk.Frame(tabs)
tabFFD6 = ttk.Frame(tabs)
tabFFD7 = ttk.Frame(tabs)
tabFFD8 = ttk.Frame(tabs)
tabFFD9 = ttk.Frame(tabs)

#creates labels for tabs
tabs.add(tabDTC, text="DTC")
tabs.add(tabFFD, text="FFD")
tabs.add(tabRTD, text="RTD")
tabs.add(tabSET, text="SET")

tabs.add(tabFFD1, text="FFD1")
tabs.add(tabFFD2, text="FFD2")
tabs.add(tabFFD3, text="FFD3")
tabs.add(tabFFD4, text="FFD4")
tabs.add(tabFFD5, text="FFD5")
tabs.add(tabFFD6, text="FFD6")
tabs.add(tabFFD7, text="FFD7")
tabs.add(tabFFD8, text="FFD8")
tabs.add(tabFFD9, text="FFD9")

#create label on DTC tab
lblDTC = ttk.Label(tabDTC, text= 'label1')
lblDTC.grid(column=0, row=0)

#create label on FFD tab
lblFFD = ttk.Label(tabFFD, text= 'label2')
lblFFD.grid(column=0, row=0)

#create image on FFD1 tab
img = ImageTk.PhotoImage( Image.open("Engine_coolant_temperature.png"))
labeEngCool = ttk.Label(tabFFD1, image = img,  text= "Test")
labeEngCool.image = img
labeEngCool.grid(column=0, row=0)

#####
testbut = Button(tabFFD2, text="Update Graph", command=updateEngineSpeed)
testbut.grid(column=0, row = 0)


#create label on RTD tab
lblRTD = ttk.Label(tabRTD, text= 'label3')
lblRTD.grid(column=0, row=0)

#create label on SET tab
lblSET = ttk.Label(tabSET, text= 'label4')
lblSET.grid(column=0, row=0)

tabs.pack(expand=1, fill='both')

#Button on the SET tab that closes the GUI when pressed
quitButton = Button(tabSET, text="Quit", command=window.destroy)
quitButton.grid(column=5, row=5)

DTCButton = Button(tabDTC, text="Look For Trouble Codes", command=runDTC)
DTCButton.grid(column=0, row = 1)

window.mainloop()


