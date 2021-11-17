#!/usr/bin/python3

#import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image
import time
import sqlite3

def updateEngineCoolantTemp():
        img = ImageTk.PhotoImage( Image.open("Engine_coolant_temperature.png"))
        labelEngineCoolantTemp = ttk.Label(tabFFD1, image = img,  text= "Test")
        labelEngineCoolantTemp.image = img
        labelEngineCoolantTemp.grid(column=0, row=1)

def updateEngineRPM():
        img = ImageTk.PhotoImage( Image.open("Engine_RPM.png"))
        labelEngSpeed = ttk.Label(tabFFD2, image = img,  text= "Test")
        labelEngSpeed.image = img
        labelEngSpeed.grid(column=0, row=1)

def updateVehicleSpeed():
        img = ImageTk.PhotoImage( Image.open("Vehicle_speed.png"))
        labelVehicleSpeed = ttk.Label(tabFFD3, image = img,  text= "Test")
        labelVehicleSpeed.image = img
        labelVehicleSpeed.grid(column=0, row=1)

def updateIntakeAirTemperature():
        img = ImageTk.PhotoImage( Image.open("Intake_air_temperature.png"))
        labelIntakeAirTemperature = ttk.Label(tabFFD4, image = img,  text= "Test")
        labelIntakeAirTemperature.image = img
        labelIntakeAirTemperature.grid(column=0, row=1)

def updateThrottlePosition():
        img = ImageTk.PhotoImage( Image.open("Throttle_position.png"))
        labelThrottlePosition = ttk.Label(tabFFD5, image = img,  text= "Test")
        labelThrottlePosition.image = img
        labelThrottlePosition.grid(column=0, row=1)

def updateCalcEngineLoad():
        img = ImageTk.PhotoImage( Image.open("Calc_engine_load.png"))
        labelFuelTankLevelInput = ttk.Label(tabFFD6, image = img,  text= "Test")
        labelFuelTankLevelInput.image = img
        labelFuelTankLevelInput.grid(column=0, row=1)

def updateAbsoluteBarometricPressure():
        img = ImageTk.PhotoImage( Image.open("Absolute_barometric_pressure.png"))
        labelFuelType = ttk.Label(tabFFD7, image = img,  text= "Test")
        labelFuelType.image = img
        labelFuelType.grid(column=0, row=1)

def updateEngineOilTemperature():
        img = ImageTk.PhotoImage( Image.open("Engine_oil_temperature.png"))
        labelEngineOilTemperature = ttk.Label(tabFFD8, image = img,  text= "Test")
        labelEngineOilTemperature.image = img
        labelEngineOilTemperature.grid(column=0, row=1)

def get_last(db, data):

	try:
		sqlcon = sqlite3.connect(db)
		cursor = sqlcon.cursor()
	except sqlite3.Error as error:
		print("ERROR, ", error)
	
	finally:
		if sqlcon:
			cursor.execute("select " + data + " from data order by datetime desc limit 1;")
			last_val = cursor.fetchall()
			cursor.close()
			sqlcon.close()
			return last_val



def runDTC():
	os.system('./DTCParse.py')
	DTC_code = get_last("DTC.db", "DTC")	
	global lblDTC
	lblDTC.destroy() 
	lblDTC = ttk.Label(tabDTC, text=DTC_code)	
	lblDTC.grid(column=0, row=0)

def runFFD():
	os.system('./FFDParse.py')
	os.system('./createGraphs.py')

def updateRuntime():
	os.system('./engineRuntime.py')
	runtime = get_last("engineRuntime.db", "Engine_runtime")
	global lblRuntime
	lblRuntime.destroy()
	lblRuntime = ttk.Label(tabFFD9, text=runtime)
	lblRuntime.grid(column=1, row=0)	

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
tabs.add(tabSET, text="Quit")

tabs.add(tabFFD1, text="FFD1")
tabs.add(tabFFD2, text="FFD2")
tabs.add(tabFFD3, text="FFD3")
tabs.add(tabFFD4, text="FFD4")
tabs.add(tabFFD5, text="FFD5")
tabs.add(tabFFD6, text="FFD6")
tabs.add(tabFFD7, text="FFD7")
tabs.add(tabFFD8, text="FFD8")
tabs.add(tabFFD9, text="FFD9")

#create label on FFD tab
lblFFD = ttk.Label(tabFFD, text= 'label2')
lblFFD.grid(column=0, row=0)

#Buttons added to each tab to update the graph
FFD1Update = Button(tabFFD1, text="Update Graph", command=updateEngineCoolantTemp)
FFD1Update.grid(column=0, row = 0)

FFD2Update = Button(tabFFD2, text="Update Graph", command=updateEngineRPM)
FFD2Update.grid(column=0, row = 0)

FFD3Update = Button(tabFFD3, text="Update Graph", command=updateVehicleSpeed)
FFD3Update.grid(column=0, row = 0)

FFD4Update = Button(tabFFD4, text="Update Graph", command=updateIntakeAirTemperature)
FFD4Update.grid(column=0, row = 0)

FFD5Update = Button(tabFFD5, text="Update Graph", command=updateThrottlePosition)
FFD5Update.grid(column=0, row = 0)

FFD6Update = Button(tabFFD6, text="Update Graph", command=updateCalcEngineLoad)
FFD6Update.grid(column=0, row = 0)

FFD7Update = Button(tabFFD7, text="Update Graph", command=updateAbsoluteBarometricPressure)
FFD7Update.grid(column=0, row = 0)

FFD8Update = Button(tabFFD8, text="Update Graph", command=updateEngineOilTemperature)
FFD8Update.grid(column=0, row = 0)

FFD9Update = Button(tabFFD9, text="Update Value", command=updateRuntime)
FFD9Update.grid(column=0, row = 1)


#create label on SET tab
#lblSET = ttk.Label(tabSET, text= 'label4')
#lblSET.grid(column=0, row=0)

tabs.pack(expand=1, fill='both')

#Button on the SET tab that closes the GUI when pressed
quitButton = Button(tabSET, text="Quit", width=20, height=10,command=window.destroy)
quitButton.grid(column=5, row=5)


#Button to search for trouble codes
DTCButton = Button(tabDTC, text="Look For Trouble Codes", command=runDTC)
DTCButton.grid(column=0, row = 1)

#create label on DTC tab
lblDTC = ttk.Label(tabDTC, text= 'Codes will appear here')
lblDTC.grid(column=0, row=0)

lblRuntime = ttk.Label(tabFFD9, text='Value will appear here')
lblRuntime.grid(column=0, row=0)

FFDCollect = Button(tabFFD, text="Collect New Data", command=runFFD)
FFDCollect.grid(column=0, row = 0)


window.mainloop()


