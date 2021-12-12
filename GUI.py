#!/usr/bin/python3

#import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image
import time
import sqlite3
import mqtt as m
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)



import DTCParse as DTCP
from getLast import get_last
import FFDParse as FFDP

broker = "broker.mqtt-dashboard.com"
port = 1883
sendTopic = "OBDIISend2"
receiveTopic = "OBDIIRec"
randomVal = random.randint(0, 1000)
client_id = "python-mqtt-%d" % randomVal
username = "emqx"
password = "public"
vol_response = "init"

client = m.connect_mqtt(client_id, broker, port, username, password)

test_data_x = [1, 2, 3, 4, 5]
test_data_y = [1, 2, 3, 7, 5]
def plot(x,y, tab):
	
	fig = Figure(figsize = (5, 5), dpi = 100)
	plot1 = fig.add_subplot(111)

	plot1.plot(y)
	canvas = FigureCanvasTkAgg(fig, master = tab)
	canvas.draw()
	canvas.get_tk_widget().pack()
	toolbar = NavigationToolbar2Tk(canvas, tab)
	toolbar.update()
	canvas.get_tk_widget().pack()


def updateEngineCoolantTemp():#engine_coolant_temp):
	# Retrieve new data
	time, engine_coolant_temp = FFDP.get_EngineCoolantTemp(client)
	
	test_data_x.append(time)
	test_data_y.append(engine_coolant_temp)
	
	labelEngineCoolantTemp = ttk.Label(tabEngCoolant)
	plot(test_data_x, test_data_y, tabEngCoolant)
	for child in tabEngCoolant.winfo_children()[1:]:
		child.destroy()
	plot(test_data_x, test_data_y, tabEngCoolant)
def updateEngineRPM(engine_rpm):
        img = ImageTk.PhotoImage( Image.open("Engine RPM.png"))
        labelEngSpeed = ttk.Label(tabEngRPM, image = img,  text= "Test")
        labelEngSpeed.image = img
        labelEngSpeed.grid(column=0, row=1)

def updateVehicleSpeed(vehicle_speed):
        img = ImageTk.PhotoImage( Image.open("Vehicle Speed.png"))
        labelVehicleSpeed = ttk.Label(tabSpeed, image = img,  text= "Test")
        labelVehicleSpeed.image = img
        labelVehicleSpeed.grid(column=0, row=1)

def updateIntakeAirTemperature(intake_air_temp):
        img = ImageTk.PhotoImage( Image.open("Intake Air Temperature.png"))
        labelIntakeAirTemperature = ttk.Label(tabIntakeAirTemp, image = img,  text= "Test")
        labelIntakeAirTemperature.image = img
        labelIntakeAirTemperature.grid(column=0, row=1)

def updateThrottlePosition(throttle_position):
        img = ImageTk.PhotoImage( Image.open("Throttle Position.png"))
        labelThrottlePosition = ttk.Label(tabThrotPos, image = img,  text= "Test")
        labelThrottlePosition.image = img
        labelThrottlePosition.grid(column=0, row=1)

def updateCalcEngineLoad(calc_engine_load):
        img = ImageTk.PhotoImage( Image.open("Calculated Engine Load.png"))
        labelCalcEngineLoad = ttk.Label(tabEngLoad, image = img,  text= "Test")
        labelCalcEngineLoad.image = img
        labelCalcEngineLoad.grid(column=0, row=1)

def updateAbsoluteBarometricPressure(absolute_barometric_pressure):
        img = ImageTk.PhotoImage( Image.open("Absolute Barometric Pressure.png"))
        labelFuelType = ttk.Label(tabBaroPres, image = img,  text= "Test")
        labelFuelType.image = img
        labelFuelType.grid(column=0, row=1)



def runDTC():
	#os.system('./DTCParse.py')
	DTC_code = DTCP.detectDTC(client)
	#DTC_code = get_last("DTC.db", "DTC")
	#DTC_code = str(DTC_code[0][0])	
	global lblDTC
	lblDTC.destroy() 
	lblDTC = ttk.Label(tabDTC, text=DTC_code)	
	lblDTC.grid(column=0, row=0)

def runFFD():
	engine_coolant_temp, engine_rpm, vehicle_speed, intake_air_temp, throttle_position, calc_engine_load, absolute_barometric_pressure = FFDP.collectFFD(client)

	updateEngineCoolantTemp(engine_coolant_temp)
	updateEngineRPM(engine_rpm)
	updateVehicleSpeed(vehicle_speed)
	updateIntakeAirTemperature(intake_air_temp)
	updateThrottlePosition(throttle_position)
	updateCalcEngineLoad(calc_engine_load)
	updateAbsoluteBarometricPressure(absolute_barometric_pressure)



def updateRuntime():
	os.system('./engineRuntime.py')
	runtime = get_last("engineRuntime.db", "Engine_runtime")
	global lblRuntime
	lblRuntime.destroy()
	print(type(runtime[0][0]))
	runtime = str(runtime[0][0]) + " Seconds" 
	lblRuntime = ttk.Label(tabEngRuntime, text=runtime)
	lblRuntime.grid(column=1, row=0)	

def clearDTC():
	os.system('./clearDTC.py')	

#Create the Window
window = Tk()

window.title("OBD-II Reader")

#Window size
#window.geometry("500x500")

#Tab Creation and Labeling
tabs = ttk.Notebook(window)
tabDTC = ttk.Frame(tabs)
tabCollectData = ttk.Frame(tabs)
tabQuit = ttk.Frame(tabs)

tabEngCoolant = ttk.Frame(tabs)
tabEngRPM = ttk.Frame(tabs)
tabSpeed = ttk.Frame(tabs)
tabIntakeAirTemp = ttk.Frame(tabs)
tabThrotPos = ttk.Frame(tabs)
tabEngLoad = ttk.Frame(tabs)
tabBaroPres = ttk.Frame(tabs)
tabEngRuntime = ttk.Frame(tabs)

#creates labels for tabs
tabs.add(tabDTC, text="DTC")
tabs.add(tabCollectData, text="Collect Data")
tabs.add(tabQuit, text="Quit")

tabs.add(tabEngCoolant, text="Engine coolant Temp")
tabs.add(tabEngRPM, text="Engine RPM")
tabs.add(tabSpeed, text="Vehicle Speed")
tabs.add(tabIntakeAirTemp, text="Intake Air Temp")
tabs.add(tabThrotPos, text="Throttle Position")
tabs.add(tabEngLoad, text="Engine Load")
tabs.add(tabBaroPres, text="Absolute Barometric Pressure")
tabs.add(tabEngRuntime, text="Engine Runtime")

#create label on CollectData tab
lblCollectData = ttk.Label(tabCollectData, text= '')
lblCollectData.grid(column=0, row=0)

#Buttons added to each tab to update the graph
EngCoolantUpdate = Button(tabEngCoolant, text="Update Graph", command=updateEngineCoolantTemp)
#EngCoolantUpdate.grid(column=0, row = 0)
EngCoolantUpdate.pack()

EngRPMUpdate = Button(tabEngRPM, text="Update Graph", command=updateEngineRPM)
EngRPMUpdate.grid(column=0, row = 0)

SpeedUpdate = Button(tabSpeed, text="Update Graph", command=updateVehicleSpeed)
SpeedUpdate.grid(column=0, row = 0)

IntakeAirTempUpdate = Button(tabIntakeAirTemp, text="Update Graph", command=updateIntakeAirTemperature)
IntakeAirTempUpdate.grid(column=0, row = 0)

ThrotPosUpdate = Button(tabThrotPos, text="Update Graph", command=updateThrottlePosition)
ThrotPosUpdate.grid(column=0, row = 0)

EngLoadUpdate = Button(tabEngLoad, text="Update Graph", command=updateCalcEngineLoad)
EngLoadUpdate.grid(column=0, row = 0)

BaroPresUpdate = Button(tabBaroPres, text="Update Graph", command=updateAbsoluteBarometricPressure)
BaroPresUpdate.grid(column=0, row = 0)

EngRuntimeUpdate = Button(tabEngRuntime, text="Update Value", command=updateRuntime)
EngRuntimeUpdate.grid(column=0, row = 1)


#create label on Quit tab
#lblQuit = ttk.Label(tabSET, text= 'label4')
#lblQuit.grid(column=0, row=0)

tabs.pack(expand=1, fill='both')

#Button on the Quit tab that closes the GUI when pressed
quitButton = Button(tabQuit, text="Quit", width=20, height=10,command=window.destroy)
quitButton.grid(column=5, row=5)


#Button to search for trouble codes
DTCButton = Button(tabDTC, text="Look For Trouble Codes", command=runDTC)
DTCButton.grid(column=0, row = 1)

DTC_clear_Button = Button(tabDTC, text="Clear Trouble Codes", command=clearDTC)
DTC_clear_Button.grid(column=0, row = 3)

#create label on DTC tab
lblDTC = ttk.Label(tabDTC, text= 'Codes will appear here')
lblDTC.grid(column=0, row=0)

lblDTC_clear = ttk.Label(tabDTC, text= '')
lblDTC_clear.grid(column=0, row=2)

lblRuntime = ttk.Label(tabEngRuntime, text='Value will appear here')
lblRuntime.grid(column=0, row=0)

CollectData = Button(tabCollectData, text="Collect New Data", command=runFFD)
CollectData.grid(column=0, row = 0)


window.mainloop()


