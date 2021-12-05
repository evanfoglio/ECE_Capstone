#!/usr/bin/python
import mqtt as m
import sys
import random
import re
import time
import sqlite3
from datetime import datetime
from paho.mqtt import client as mqtt
#MQTT#######################################################

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
#time.sleep(.5)

def on_message(client, userdata, msg):
                message = "%s" % msg.payload.decode()
                global vol_response
                vol_response = message
m.subscribe(client, "OBDIIRec")
client.on_message = on_message

def sql_export(dtc):
	#export into SQL
	try:
		sqlcon = sqlite3.connect("DTC.db")
		cursor = sqlcon.cursor()
		#insert collected data into the sqlite3 string
		insertdata = "insert into data(DTC, datetime) values (\"{}\", \"{}\")".format( dtc, datetime.now())
		count = cursor.execute(insertdata)
		sqlcon.commit()
		cursor.close()
	#Error checking
	except sqlite3.Error as error:
		print("ERROR, ", error)
	
	finally:
		if sqlcon:
			sqlcon.close()



if __name__ == "__main__":
	print("\n\n\n\n\n\n\n")
	#Send Mode 1 PID 01 requset
	# >01 01
	#Typical Response:
	#41 01 81 07 65 04
	
	####
	#SEND REQUEST TBD
	####

	prev_response = vol_response
	client.loop()
	m.publish(client, "OBDIISend2", "01 01")
	
	####
        # RECEIVE RESPONSE
        ####
	m.subscribe(client, "OBDIIRec")
	while vol_response == prev_response:
		time.sleep(.1)
		client.loop()	
	
	#Respone comes as unicode,
	str_response = str(vol_response)
	print(str_response)
	#separate received string into individule values
	#Not needed for current simulations but will be needed in the future
	split_response = str_response.split()
	
	#DEBUG
	print("\nSplit: ")
	print(split_response)	
	
	print("\nSplit[0]: ")
        print(split_response[0])	


	if ((split_response[2] != '41') and (split_response[3] != '01')):
		#invalid relpy
		print("Invalid reply after first message")
		sys.exit(0)

	#case for 0 codes
	if(split_response[4] == '00'):
		code = "No Codes"
		sql_export(code)
		quit()

	intErrorCode = int(split_response[3], 16)
	if intErrorCode < 0x80:
		#Check Engine Lamp or MIL is not on
		nErrorCodes = split_response[3]	
	else:
		#lights are on
        	nErrorCodes = intErrorCode - 0x80

	#Find Actual trouble codes
	#Send mode switch command

	###
	# > 03
	###

	prev_response = vol_response
        client.loop()
	#send 03 to Remote system to switch ELM327 Modes
        m.publish(client, "OBDIIRec","03")
	while vol_response == prev_response:
                time.sleep(.1)
                client.loop()
	str_response = str(vol_response)

	#possible response:
	#43 01 33 00 00 00 00
	# 43 says its a mode 3 response,
	
	#error check, 43 indicates a response in mode 3
	print(str_response)
	str_response = str_response.split()
	
	print(str_response)

	if str_response[1] != '43':
	        print("invalid response")
	        sys.exit(0)
	print(str_response)
	# Next 6 bytes are read in pairs,
        # Ex: 0133 0000 0000
        #by standard it is padded with 0s, 0000 do not represent trouble codes
	str_response.pop(0) # remove the first value, it is just used for confirmation
	refined_response = [str_response[0] + str_response[1], str_response[2] + str_response[3], str_response[4] + str_response[5]]
	refined_response = [i for i in refined_response if i != "0000"]	


	DTC_dict = { 
		"0":"P0",
		"1":"P1",
		"2":"P2",
		"3":"P3",
		"4":"C0",
		"5":"C1",
		"6":"C2",
		"7":"C3",
		"8":"B0",
		"9":"B1",
		"A":"B2",
		"B":"B3",
		"C":"U0",
		"D":"U1",
		"E":"U2",
		"F":"U3"}
	
	#bytes of the retuen values are combined and decoded usinf the DTC_dict, values found
	# in ELM327 data sheet
	parsedDTC = [0, 0, 0]
	for i in range(len(refined_response)): 
		parsedDTC[i] = DTC_dict[refined_response[i][0]] + refined_response[i][1:]	


	for i in parsedDTC:
		if i != 0:
			sql_export(i)	










		
	
 
