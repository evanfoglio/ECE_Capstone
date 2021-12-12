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


EngCoolant_x = []
EngCoolant_y = []

EngRPM_x = []
EngRPM_y = []

Speed_x = []
Speed_y = []

IntakeAirTemp_x = []
IntakeAirTemp_y = []

ThrotPos_x = []
ThrotPos_y = []

EngLoad_x = []
EngLoad_y = []

BaroPres_x = []
BaroPres_y = []


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

	#append new data to the global array	
	EngCoolant_x.append(time)
	EngCoolant_y.append(engine_coolant_temp)
	
	#Destroy all the children on the tab, excluding the first element,
	# the button to update the graph
	for child in tabEngCoolant.winfo_children()[1:]:
		child.destroy()
	#plot the new data on  the notebook tab
	plot(EngCoolant_x, EngCoolant_y, tabEngCoolant)

def updateEngineRPM():
        # Retrieve new data
        time, engine_rpm = FFDP.get_EngineRPM(client)

        #append new data to the global array
        EngRPM_x.append(time)
        EngRPM_y.append(engine_rpm)

        #Destroy all the children on the tab, excluding the first element,
        # the button to update the graph
        for child in tabEngRPM.winfo_children()[1:]:
                child.destroy()
        #plot the new data on  the notebook tab
        plot(EngRPM_x, EngRPM_y, tabEngRPM)


def updateVehicleSpeed():
        # Retrieve new data
        time, vehicle_speed = FFDP.get_VehicleSpeed(client)

        #append new data to the global array
        Speed_x.append(time)
        Speed_y.append(vehicle_speed)

        #Destroy all the children on the tab, excluding the first element,
        # the button to update the graph
        for child in tabSpeed.winfo_children()[1:]:
                child.destroy()
        #plot the new data on  the notebook tab
        plot(Speed_x, Speed_y, tabSpeed)


def updateIntakeAirTemperature():
        # Retrieve new data
        time, intake_air_temp = FFDP.get_IntakeAirTemp(client)

        #append new data to the global array
        IntakeAirTemp_x.append(time)
        IntakeAirTemp_y.append(intake_air_temp)

        #Destroy all the children on the tab, excluding the first element,
        # the button to update the graph
        for child in tabIntakeAirTemp.winfo_children()[1:]:
                child.destroy()
        #plot the new data on  the notebook tab
        plot(IntakeAirTemp_x, IntakeAirTemp_y, tabIntakeAirTemp)


def updateThrottlePosition():
        # Retrieve new data
        time, throttle_position = FFDP.get_ThrottlePos(client)

        #append new data to the global array
        ThrotPos_x.append(time)
        ThrotPos_y.append(throttle_position)

        #Destroy all the children on the tab, excluding the first element,
        # the button to update the graph
        for child in tabThrotPos.winfo_children()[1:]:
                child.destroy()
        #plot the new data on  the notebook tab
        plot(ThrotPos_x, ThrotPos_y, tabThrotPos)


def updateCalcEngineLoad():
        # Retrieve new data
        time, calc_engine_load = FFDP.get_EngineLoad(client)

        #append new data to the global array
        EngLoad_x.append(time)
        EngLoad_y.append(calc_engine_load)

        #Destroy all the children on the tab, excluding the first element,
        # the button to update the graph
        for child in tabEngLoad.winfo_children()[1:]:
                child.destroy()
        #plot the new data on  the notebook tab
        plot(EngLoad_x, EngLoad_y, tabEngLoad)


def updateAbsoluteBarometricPressure():
        # Retrieve new data
        time, absolute_barometric_pressure = FFDP.get_AbsBarometricPressure(client)

        #append new data to the global array
        BaroPres_x.append(time)
        BaroPres_y.append(absolute_barometric_pressure)

        #Destroy all the children on the tab, excluding the first element,
        # the button to update the graph
        for child in tabBaroPres.winfo_children()[1:]:
                child.destroy()
        #plot the new data on  the notebook tab
        plot(BaroPres_x, BaroPres_y, tabBaroPres)




def runDTC():
	DTC_code = DTCP.detectDTC(client)
	#DTC_code = get_last("DTC.db", "DTC")
	#DTC_code = str(DTC_code[0][0])	
	global lblDTC
	lblDTC.destroy() 
	lblDTC = ttk.Label(tabDTC, text=DTC_code)	
	lblDTC.grid(column=0, row=0)

def runFFD():
	#engine_coolant_temp, engine_rpm, vehicle_speed, intake_air_temp, throttle_position, calc_engine_load, absolute_barometric_pressure = FFDP.collectFFD(client)

	updateEngineCoolantTemp()
	updateEngineRPM()
	updateVehicleSpeed()
	updateIntakeAirTemperature()
	updateThrottlePosition()
	updateCalcEngineLoad()
	updateAbsoluteBarometricPressure()



def updateRuntime():
	runtime = FFDP.get_Runtime(client)
	global lblRuntime
	lblRuntime.destroy()
	runtime = str(runtime) + " Seconds" 
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
EngCoolantUpdate.pack()#

EngRPMUpdate = Button(tabEngRPM, text="Update Graph", command=updateEngineRPM)
EngRPMUpdate.pack()#.grid(column=0, row = 0)

SpeedUpdate = Button(tabSpeed, text="Update Graph", command=updateVehicleSpeed)
SpeedUpdate.pack()#.grid(column=0, row = 0)

IntakeAirTempUpdate = Button(tabIntakeAirTemp, text="Update Graph", command=updateIntakeAirTemperature)
IntakeAirTempUpdate.pack()#.grid(column=0, row = 0)

ThrotPosUpdate = Button(tabThrotPos, text="Update Graph", command=updateThrottlePosition)
ThrotPosUpdate.pack()#.grid(column=0, row = 0)

EngLoadUpdate = Button(tabEngLoad, text="Update Graph", command=updateCalcEngineLoad)
EngLoadUpdate.pack()#.grid(column=0, row = 0)

BaroPresUpdate = Button(tabBaroPres, text="Update Graph", command=updateAbsoluteBarometricPressure)
BaroPresUpdate.pack()#.grid(column=0, row = 0)

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


