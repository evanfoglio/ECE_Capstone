#!/usr/bin/python3

import tkinter as tk

from tkinter import ttk

window = tk.Tk()

window.title("OBD-II Reader")

window.geometry("500x500")

tabs = ttk.Notebook(window)
tabDTC = ttk.Frame(tabs)
tabFFD = ttk.Frame(tabs)
tabRTD = ttk.Frame(tabs)

tabs.add(tabDTC, text="DTC")
tabs.add(tabFFD, text="FFD")
tabs.add(tabRTD, text="RTD")

lblDTC = ttk.Label(tabDTC, text= 'label1')
lblDTC.grid(column=0, row=0)

lblFFD = ttk.Label(tabFFD, text= 'label2')
lblFFD.grid(column=0, row=0)

lblRTD = ttk.Label(tabRTD, text= 'label3')
lblRTD.grid(column=0, row=0)


tabs.pack(expand=1, fill='both')

window.mainloop()


