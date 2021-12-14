#!/usr/bin/python
import mqtt as m
import random
import time
import sqlite3
from datetime import datetime
import sys

def one_byte_response(cmd, client):

	global message_flag
	message_flag = False
        #define the on_message callback function
	def on_message(client, userdata, msg):
		message = "%s" % msg.payload.decode()
		global vol_response
		global message_flag
		message_flag = True
		vol_response = message
	client.on_message = on_message

	#SEND AT 01 cmd
	at_cmd = "01 %s\n" % cmd
	m.subscribe(client, "OBDIIRec")
	m.publish(client, "OBDIISend2", at_cmd)
	
	#RECEIVE 41 cmd data
	#wait for global message_flag
	while (not message_flag):
                client.loop()
	#reset flag
	message_flag = False
		
	response = (str(vol_response)).split()
	#check to make sure it fits min length
	if((len(response) < 4)):
                #bad response
                log("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
                print("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
                sys.exit(0)

	#check to make sure response is valid relpy
	if response[2] != '41' and response[3] != cmd:
		#bad response
		log("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
		print("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
		sys.exit(0)
	else:	#Return 3rd byte
		return response[4]

def two_byte_response(cmd, client):
        
	global message_flag
	message_flag = False
	#define the on_message callback function
	def on_message(client, userdata, msg):
		message = "%s" % msg.payload.decode()
		global vol_response
		global message_flag
		message_flag = True
		vol_response = message
	client.on_message = on_message


	#SEND AT 01 cmd
	at_cmd = "01 %s" % cmd
	m.subscribe(client, "OBDIIRec")
	m.publish(client, "OBDIISend2", at_cmd)

        #RECEIVE 41 cmd data
	while (not message_flag):
		client.loop()
	#reset global message flag
	message_flag = False
	response = (str(vol_response)).split()
	#check to make sure it fits min length
	if((len(response) < 4)):
                #bad response
		log("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
		print("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
		sys.exit(0)
	#check to make sure response is valid relpy
	if response[2] != '41' and response[3] != cmd:
                #bad response
                log("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
                print("Invalid reply to 01 " + cmd + " in FFDParse.py: " + str(response))
                sys.exit(0)
	else:  	#Return 3rd and 4th byte
		return [response[4], response[5]]

#log func for logging errors
def log(text):
        #open log file with appened
        f = open("log.txt", "a")
        f.write(str(datetime.now())+ "\t"  + text + "\n")


#All "get_X" functions querry with their specific PID and equation
# for translating the bytes to the actual value
def get_EngineCoolantTemp(client):
	engine_coolant_temp = int(one_byte_response("05", client), 16) - 40
	sql_export("FFD.db", "EngCoolTemp", "temp", engine_coolant_temp)
	return datetime.now(), engine_coolant_temp
def get_EngineRPM(client):
        engine_rpm_bytes = two_byte_response("0C", client)
        engine_rpm_bytes[0] = int(engine_rpm_bytes[0], 16)
        engine_rpm_bytes[1] = int(engine_rpm_bytes[1], 16)
        engine_rpm = (256 * engine_rpm_bytes[0] + engine_rpm_bytes[1]) / 4
        sql_export("FFD.db", "EngRPM", "rpm", engine_rpm)
        return datetime.now(), engine_rpm

def get_VehicleSpeed(client):
	vehicle_speed = int(one_byte_response("0D", client), 16)
	sql_export("FFD.db", "VehicleSpeed", "speed", vehicle_speed)
	return datetime.now(), vehicle_speed
def get_IntakeAirTemp(client):
	intake_air_temp = int(one_byte_response("0F", client), 16) - 40
	sql_export("FFD.db", "IntakeAriTemp", "temp", intake_air_temp)
	return datetime.now(), intake_air_temp

def get_ThrottlePos(client):
	throttle_position = int(one_byte_response("11", client), 16) * (100.0/255.0)
	sql_export("FFD.db", "throttle_position", "pos", throttle_position)
	return datetime.now(), throttle_position

def get_EngineLoad(client):
	calc_engine_load = int(one_byte_response("04", client), 16) * (100.0/255.0)
	sql_export("FFD.db", "EngLoad", "load", calc_engine_load)
	return datetime.now(), calc_engine_load

def get_AbsBarometricPressure(client):
	absolute_barometric_pressure = int(one_byte_response("33", client), 16)
	sql_export("FFD.db", "AbsBaroPres", "pressure", absolute_barometric_pressure)
	return datetime.now(), absolute_barometric_pressure

def get_Runtime(client):
        engine_runtime_bytes = two_byte_response("1F", client)
        engine_runtime_bytes[0] = int(engine_runtime_bytes[0], 16)
        engine_runtime_bytes[1] = int(engine_runtime_bytes[1], 16)
        engine_runtime = (256 * engine_runtime_bytes[0]) + engine_runtime_bytes[1]
        sql_export("FFD.db", "Runtime", "runtime", engine_runtime)
        return engine_runtime



def sql_export(database, tablename, dataname, data):
        #export into SQL
        try:
                sqlcon = sqlite3.connect(database)
                cursor = sqlcon.cursor()
                #insert collected data into the sqlite3 string
                insertdata = "insert into {}({}, datetime) values (\"{}\", \"{}\")".format(tablename, dataname, data, datetime.now())
                count = cursor.execute(insertdata)
                sqlcon.commit()
                cursor.close()
        #Error checking
        except sqlite3.Error as error:
                print("ERROR, ", error)

        finally:
                if sqlcon:
                        sqlcon.close()


















