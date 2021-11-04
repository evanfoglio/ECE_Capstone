#!/usr/bin/python3
import matplotlib.pyplot as plt
import time
import sqlite3
import numpy as np
# Database
try:
        sqlcon = sqlite3.connect('FFD.db')
        cursor = sqlcon.cursor()
except sqlite3.Error as error:
        print("ERROR, ", error)

finally:
        if sqlcon:
                cursor.execute("select * from data")#'select 
				#Engine_coolant_temperature,
				#Fuel_pressure, 
				#Engine_speed, 
				#Vehicle_speed, 
				#Intake_air_temperature,
				#Throttle_position,
				#Fuel_Tank_Level_Input,
				#Fuel_Type,
				#datetime
				#from data')
                data = cursor.fetchall()
                cursor.close()
                sqlcon.close()

#initialize arrays for data
Engine_coolant_temperature = []
Fuel_pressure = []
Engine_speed = []
Vehicle_speed = []
Intake_air_temperature = []
Throttle_position = []
Fuel_Tank_Level_Input = []
Fuel_Type = []
Engine_oil_temperature = []
datetime = []
for row in data:
	Engine_coolant_temperature.append(row[0])
	Fuel_pressure.append(row[1])
	Engine_speed.append(row[2])
	Vehicle_speed.append(row[3])
	Intake_air_temperature.append(row[4])
	Throttle_position.append(row[5])
	Fuel_Tank_Level_Input.append(row[6])
	Fuel_Type.append(row[7])
	Engine_oil_temperature.append(row[8])
	datetime.append(row[9])


data = [Engine_coolant_temperature, 
	Fuel_pressure, 
	Engine_speed, 
	Vehicle_speed, 
	Intake_air_temperature, 
	Throttle_position, 
	Fuel_Tank_Level_Input, 
	Fuel_Type, 
	Engine_oil_temperature]

graph_labelsY = ["Temperature", 
		"Pressure", 
		"Speed", 
		"Speed", 
		"Temperature", 
		"Position", 
		"Fuel_Tank_Level_Input", 
		"Fuel_Type", 
		"Temperature"]

graph_titles = ["Engine_coolant_temperature", 
		"Fuel_pressure", 
		"Engine_speed", 
		"Vehicle_speed", 
		"Intake_air_temperature", 
		"Throttle_position", 
		"Fuel_Tank_Level_Input",
		"Fuel_Type",
		"Engine_oil_temperature"]

export_names = [s + ".png" for s in graph_titles]

for i in range(9):
	temp_fig, ax = plt.subplots(1)
	temp_fig.set_size_inches(8, 6)
	plt.plot(datetime, data[i])
	plt.xlabel("Time")
	plt.ylabel(graph_labelsY[i])
	plt.title(graph_titles[i])
	plt.xticks(rotation = -45, ha="left", rotation_mode="anchor")
	# Limit x-axis to 12 tick marks
	ax.xaxis.set_major_locator(plt.MaxNLocator(12))
	# Format to not cut off part of the dats on x-axis
	plt.tight_layout()
	#export to PNG for webserver displying
	plt.savefig(export_names[i])

