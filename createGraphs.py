#!/usr/bin/python3
#import matplotlib.pyplot as plt
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


