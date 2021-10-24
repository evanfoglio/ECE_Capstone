#!/usr/bin/python
import mqtt as m
import random
import time
import sqlite3
from datetime import datetime
import sys

broker = "broker.mqtt-dashboard.com"
port = 1883
sendTopic = "OBDIIRec"
receiveTopic = "OBDIISend"
randomVal = random.randint(0, 1000)
client_id = "python-mqtt-%d" % randomVal
username = "emqx"
password = "public"
vol_response = "init"

client = m.connect_mqtt(client_id, broker, port, username, password)
time.sleep(3)

def on_message(client, userdata, msg):
                message = "%s" % msg.payload.decode()
                global vol_response
                vol_response = message
m.subscribe(client, "OBDIISend")
client.on_message = on_message

def one_byte_response(cmd):
	#SEND AT 01 cmd
	prev_response = vol_response
	at_cmd = "AT 01 %s" % cmd
	m.publish(client, "OBDIIRec", at_cmd)
	
	#RECEIVE 41 cmd data
	while vol_response == prev_response:
                time.sleep(.1)
                client.loop()
		
	response = (str(vol_response)).split()
	
	if response[0] != '41' and response[1] != cmd:
		#bad response
		print("Invalid response, exiting")
		sys.exit(0)
	else:	#Return 3rd byte
		return response[2]

def two_byte_response(cmd):
        #SEND AT 01 cmd
        prev_response = vol_response
        at_cmd = "AT 01 %s" % cmd
        m.publish(client, "OBDIIRec", at_cmd)

        #RECEIVE 41 cmd data
        while vol_response == prev_response:
                time.sleep(.1)
                client.loop()

        response = (str(vol_response)).split()

        if response[0] != '41' and response[1] != cmd:
                #bad response
                print("Invalid response, exiting")
                sys.exit(0)
        else:   #Return 3rd byte
                return [response[2], response[3]]



if __name__ == "__main__":
	

	#find eningine coolant temp (degree C)
	engine_coolant_temp = int(one_byte_response("05"), 16) - 40		
        
	time.sleep(.1)
	
	#Find fuel pressure
	fuel_pressure = 3 * int(one_byte_response("0A"))

	time.sleep(.1)
	
	#find Engine RPM	
	engine_rpm_bytes = two_byte_response("0C")
	engine_rpm_bytes[0] = int(engine_rpm_bytes[0], 16)
	engine_rpm_bytes[1] = int(engine_rpm_bytes[1], 16)
	engine_rpm = (256 * engine_rpm_bytes[0] + engine_rpm_bytes[1]) / 4

	time.sleep(.1)
	#find vehicle speed (km/h)
	vehicle_speed = one_byte_response("0D")

	time.sleep(.1)
	
	#find intake air temp (degree C)
	intake_air_temp = int(one_byte_response("0F"), 16) - 40

	time.sleep(.1)

	#find throttle position (%)
	throttle_position = int(one_byte_response("11"), 16) * (100/255)

	time.sleep(.1)
	
	#find fuel tank level input (%)
	fuel_tank_level_input = int(one_byte_response("2F"), 16) * (100/255)



	 #export into SQL
        try:
                sqlcon = sqlite3.connect("FFD.db")
                cursor = sqlcon.cursor()
                #insert collected data into the sqlite3 string
                insertdata = "insert into data(Engine_coolant_temperature, Fuel_pressure, Engine_speed, Vehicle_speed , Intake_air_temperature, Throttle_position, Fuel_Tank_Level_Input, Fuel_Type, Engine_oil_temperature, datetime) values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(engine_coolant_temp, fuel_pressure, engine_rpm, vehicle_speed, fuel_tank_level_input, "N/A", "N/A", "N/A", "N/A", datetime.now())
		count = cursor.execute(insertdata)
                sqlcon.commit()
                cursor.close()
        #Error checking
        except sqlite3.Error as error:
                print("ERROR, ", error)

        finally:
                if sqlcon:
                        sqlcon.close()






















