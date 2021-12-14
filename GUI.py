#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import time
import mqtt as m
import random
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import DTCParse as DTCP
import FFDParse as FFDP

#Broker Credentials
broker = "broker.mqtt-dashboard.com"
port = 1883
sendTopic = "OBDIISend2"
receiveTopic = "OBDIIRec"
randomVal = random.randint(0, 1000)
client_id = "python-mqtt-%d" % randomVal
username = "emqx"
password = "public"
vol_response = "init"

#client is passed to functions wanting to connect to the remote system
client = m.connect_mqtt(client_id, broker, port, username, password)

#Global array variables for each type of data collected
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

#plotting function takes in the x,y data as well as the tab 
# the plot is to go on
def plot(x, y, tab, ylabel, title):
	#Create the figure,
	# 6 inch by 6 inch
	# dots per inch, dpi, 100
	# facecolor to match default gui color
	fig = Figure(figsize = (6, 6), dpi = 100, facecolor = '#d9d9d9')

	plot1 = fig.add_subplot(111)

	#plot the data
	plot1.plot(x,y)
	
	#set labels
	plot1.set_ylabel(ylabel)
	plot1.set_xlabel("Time")
	
	#rotate the X ticks to be readable
	for tick in plot1.get_xticklabels():
		tick.set_rotation(45)
	
	plot1.title.set_text(title)
	
	#set the plot to be on the passed notebook tab
	canvas = FigureCanvasTkAgg(fig, master = tab)
	canvas.draw()
	#pack the gragh
	canvas.get_tk_widget().pack()
	
	#configure the toolbar to affect the plot and set it to the passed tab
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
	plot(EngCoolant_x, EngCoolant_y, tabEngCoolant, "Degree Celsius", "Engine Coolant Temperature")

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
        plot(EngRPM_x, EngRPM_y, tabEngRPM, "RPM", "Engine RPM")


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
        plot(Speed_x, Speed_y, tabSpeed, "Km/h", "Vehicle Speed")


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
        plot(IntakeAirTemp_x, IntakeAirTemp_y, tabIntakeAirTemp, "Degree Celsius", "Intake Air Temperature")


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
        plot(ThrotPos_x, ThrotPos_y, tabThrotPos, "%", "Throttle Position")


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
        plot(EngLoad_x, EngLoad_y, tabEngLoad, "%", "Calculated Engine Load")


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
        plot(BaroPres_x, BaroPres_y, tabBaroPres, "KPa", "Absolute Barometric Pressure")



#runDTC finds trouble codes and updates the label on the DTC notebook tab
def runDTC():
	#find trouble codes
	DTC_code = DTCP.detectDTC(client)
	#get the label
	global lblDTC
	#destroy old label
	lblDTC.destroy() 
	#create new label with found/not found codes
	lblDTC = ttk.Label(tabDTC, text=DTC_code)
	#place the label	
	lblDTC.grid(column=0, row=0)

#runFFD runs all the update data functions allowing faster data collection 
def runFFD():
	#call all update functions for mass data collection
	updateEngineCoolantTemp()
	updateEngineRPM()
	updateVehicleSpeed()
	updateIntakeAirTemperature()
	updateThrottlePosition()
	updateCalcEngineLoad()
	updateAbsoluteBarometricPressure()


#Retrives the current engine runtime and updates the label on Engine Runtime tab
def updateRuntime():
	#get runtime
	runtime = FFDP.get_Runtime(client)
	#get the label
	global lblRuntime
	#destroy the old label
	lblRuntime.destroy()
	#add units
	runtime = str(runtime) + " Seconds" 
	#create the new label
	lblRuntime = ttk.Label(tabEngRuntime, text=runtime)
	#place the new label
	lblRuntime.grid(column=1, row=0)	


def clearDTC():
	DTCP.clearDTC(client)

#Create the master Window
window = Tk()

window.title("OBD-II Reader")

#Tab Creation and Labeling
#create the tabs based on the master window
tabs = ttk.Notebook(window)

#create specific tabs based on the tabs object
tabDTC = ttk.Frame(tabs)
tabCollectData = ttk.Frame(tabs)
tabQuit = ttk.Frame(tabs)

#notebook tabs for the various data types
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
EngCoolantUpdate.pack()

EngRPMUpdate = Button(tabEngRPM, text="Update Graph", command=updateEngineRPM)
EngRPMUpdate.pack()

SpeedUpdate = Button(tabSpeed, text="Update Graph", command=updateVehicleSpeed)
SpeedUpdate.pack()

IntakeAirTempUpdate = Button(tabIntakeAirTemp, text="Update Graph", command=updateIntakeAirTemperature)
IntakeAirTempUpdate.pack()

ThrotPosUpdate = Button(tabThrotPos, text="Update Graph", command=updateThrottlePosition)
ThrotPosUpdate.pack()

EngLoadUpdate = Button(tabEngLoad, text="Update Graph", command=updateCalcEngineLoad)
EngLoadUpdate.pack()

BaroPresUpdate = Button(tabBaroPres, text="Update Graph", command=updateAbsoluteBarometricPressure)
BaroPresUpdate.pack()

EngRuntimeUpdate = Button(tabEngRuntime, text="Update Value", command=updateRuntime)
EngRuntimeUpdate.grid(column=0, row = 1)

tabs.pack(expand=1, fill='both')

#Button on the Quit tab that closes the GUI when pressed, destroys master window
quitButton = Button(tabQuit, text="Quit", width=20, height=10,command=window.destroy)
quitButton.pack()

#create label where the DTC codes will be placed
lblDTC = ttk.Label(tabDTC, text= 'Codes will appear here')
lblDTC.grid(column=0, row=0)


#Button to search for trouble codes
DTCButton = Button(tabDTC, text="Look For Trouble Codes", command=runDTC)
DTCButton.grid(column=0, row = 1)

#create button to clear the DTC codes, place on the DTC tab
DTC_clear_Button = Button(tabDTC, text="Clear Trouble Codes", command=clearDTC)
DTC_clear_Button.grid(column=0, row = 3)

#create clear DTC label on DTC tab
lblDTC_clear = ttk.Label(tabDTC, text= '')
lblDTC_clear.grid(column=0, row=2)

#create label for runtime value to be updated to
lblRuntime = ttk.Label(tabEngRuntime, text='Value will appear here')
lblRuntime.grid(column=0, row=0)

#create button to run mass collect data
CollectData = Button(tabCollectData, text="Collect New Data", command=runFFD)
CollectData.grid(column=0, row = 0)

#master window loop
window.mainloop()


