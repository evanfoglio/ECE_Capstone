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
                cursor.execute("select
				Engine_coolant_temperature, 
				Engine_RPM, 
				Vehicle_speed, 
				Intake_air_temperature,
				Throttle_position,
				Absolute_barometric_pressure,
				Engine_oil_temperature,
				datetime
				from data;")
                data = cursor.fetchall()
                cursor.close()
                sqlcon.close()

#initialize arrays for data
Engine_coolant_temperature = []
Engine_RPM = []
Vehicle_speed = []
Intake_air_temperature = []
Throttle_position = []
Calc_engine_load = []
Absolute_barometric_pressure = []
Engine_oil_temperature = []
datetime = []
for row in data:
	Engine_coolant_temperature.append(int(row[0]))
	Fuel_pressure.append(int(row[1]))
	Engine_RPM.append(int(row[2]))
	Vehicle_speed.append(int(row[3]))
	Intake_air_temperature.append(int(row[4]))
	Throttle_position.append(int(row[5]))
	Calc_engine_load.append(int(row[6]))
	Absolute_barometric_pressure.append(int(row[7]))
	Engine_oil_temperature.append(int(row[8]))
	datetime.append(row[9])


data = [Engine_coolant_temperature, 
	Fuel_pressure, 
	Engine_RPM, 
	Vehicle_speed, 
	Intake_air_temperature, 
	Throttle_position, 
	Calc_engine_load, 
	Absolute_barometric_pressure, 
	Engine_oil_temperature]

graph_labelsY = ["Temperature", 
		"Pressure", 
		"RPM", 
		"Speed", 
		"Temperature", 
		"Position", 
		"Calc_engine_load", 
		"Absolute_barometric_pressure", 
		"Temperature"]

graph_titles = ["Engine_coolant_temperature", 
		"Fuel_pressure", 
		"Engine_RPM", 
		"Vehicle_speed", 
		"Intake_air_temperature", 
		"Throttle_position", 
		"Calc_engine_load",
		"Absolute_barometric_pressure",
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

