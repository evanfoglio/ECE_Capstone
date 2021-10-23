#!/usr/bin/python3

import tkinter as tk

from tkinter import ttk

#Create the Window
window = tk.Tk()

window.title("OBD-II Reader")

#Window size
window.geometry("500x500")

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

lblRTD = ttk.Label(tabRTD, text= 'label3')
lblRTD.grid(column=0, row=0)

lblSET = ttk.Label(tabSET, text= 'label4')
lblSET.grid(column=0, row=0)

tabs.pack(expand=1, fill='both')

#Button on the SET tab that closes the GUI when pressed
quitButton = ttk.Button(tabSET, text="Quit", command=window.destroy)
quitButton.grid(column=5, row=5)


window.mainloop()


