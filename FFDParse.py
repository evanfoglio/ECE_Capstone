#!/usr/bin/python
import mqtt as m
import random
import time
import sqlite3
from datetime import datetime
import sys

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
time.sleep(1)



message_flag = False
def on_message(client, userdata, msg):
	message = "%s" % msg.payload.decode()
	global vol_response
	global message_flag
	vol_response = message
	message_flag = True

m.subscribe(client, "OBDIIRec")
client.on_message = on_message

def one_byte_response(cmd):
	#SEND AT 01 cmd
	prev_response = vol_response
	at_cmd = "01 %s\n" % cmd
	m.publish(client, "OBDIISend2", at_cmd)
	
	#RECEIVE 41 cmd data
	global message_flag
	while (not message_flag):
                time.sleep(.1)
                client.loop()
	message_flag = False
		
	response = (str(vol_response)).split()
	print(response)
	if response[2] != '41' and response[3] != cmd:
		#bad response
		log("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
                print("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
		sys.exit(0)
	else:	#Return 3rd byte
		return response[4]

def two_byte_response(cmd):
        #SEND AT 01 cmd
	prev_response = vol_response
	at_cmd = "01 %s" % cmd
	m.publish(client, "OBDIISend2", at_cmd)

        #RECEIVE 41 cmd data
	global message_flag
	while (not message_flag):
		time.sleep(.1)
		client.loop()
	message_flag = False
	response = (str(vol_response)).split()

	if response[2] != '41' and response[3] != cmd:
                #bad response
		log("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
                print("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
		sys.exit(0)
	else:  	#Return 3rd byte
		return [response[4], response[5]]


def log(text):
        #open log file with appened
        f = open("log.txt", "a")
        f.write(str(datetime.now())+ "\t"  + text + "\n")




if __name__ == "__main__":
	

	#find eningine coolant temp (degree C)
	engine_coolant_temp = int(one_byte_response("05"), 16) - 40		
	
	#find Engine RPM	
	engine_rpm_bytes = two_byte_response("0C")
	engine_rpm_bytes[0] = int(engine_rpm_bytes[0], 16)
	engine_rpm_bytes[1] = int(engine_rpm_bytes[1], 16)
	engine_rpm = (256 * engine_rpm_bytes[0] + engine_rpm_bytes[1]) / 4

	time.sleep(.1)
	#find vehicle speed (km/h)
	vehicle_speed = int(one_byte_response("0D"), 16)
	
	#find intake air temp (degree C)
	intake_air_temp = int(one_byte_response("0F"), 16) - 40

	#find throttle position (%)
	throttle_position = int(one_byte_response("11"), 16) * (100.0/255.0)
	
	#find the engine load (%)
	calc_engine_load = int(one_byte_response("04"), 16) * (100.0/255.0)
	
	#find the absolute_barometric_pressure (kpa)
	absolute_barometric_pressure = int(one_byte_response("33"))
	
	#export into SQL
	try:
		#sqlcon = sqlite3.connect("school/capstone/FFD.db")
		sqlcon = sqlite3.connect("FFD.db")
		cursor = sqlcon.cursor()
                #insert collected data into the sqlite3 string
		insertdata = "insert into data(Engine_coolant_temperature, Engine_RPM, Vehicle_speed , Intake_air_temperature, Throttle_position, Calc_engine_load, Absolute_barometric_pressure, datetime) values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(engine_coolant_temp, engine_rpm, vehicle_speed, intake_air_temp, throttle_position, calc_engine_load, absolute_barometric_pressure, datetime.now())

		count = cursor.execute(insertdata)
		sqlcon.commit()
		cursor.close()
        #Error checking
	except sqlite3.Error as error:
		print("ERROR, ", error)
	finally:
		if sqlcon:
			sqlcon.close()






















