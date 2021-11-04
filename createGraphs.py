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
                cursor.execute('select 
				Engine_coolant_temperature,
				Fuel_pressure, 
				Engine_speed, 
				Vehicle_speed, 
				Intake_air_temperature,
				Throttle_position,
				Fuel_Tank_Level_Input,
				Fuel_Type
				from data')
                data = cursor.fetchall()
                cursor.close()
                sqlcon.close()

