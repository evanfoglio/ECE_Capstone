#!/usr/bin/python
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
sendTopic = "OBDIIRec"
receiveTopic = "OBDIISend"
randomVal = random.randint(0, 1000)
client_id = "python-mqtt-%d" % randomVal

username = "emqx"
password = "public"

response = "init"

def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
                if rc == 0:
                        print("Connected to MQTT Broker!")
                else:
                        print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        client = mqtt.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client


def subscribe(client):
        def on_message(client, userdata, msg):
		message = "%s" % msg.payload.decode()
		global response 
		response = message
        client.subscribe(receiveTopic)
        client.on_message = on_message


client = connect_mqtt()
time.sleep(3)
def publish(client, msg):
        result = client.publish(sendTopic, msg)
        # result: [0, 1]
        status = result[0]
        if status != 0:
                print("Failed to send message")
###########################################################


if __name__ == "__main__":

	#Send Mode 1 PID 01 requset
	# >01 01
	#Typical Response:
	#41 01 81 07 65 04
	
	####
	#SEND REQUEST TBD
	####

	prev_response = response
	client.loop()
	publish(client, "01 01")
	
	####
        # RECEIVE RESPONSE TBD
        ####
	subscribe(client)
	while response == prev_response:
		time.sleep(.1)
		client.loop()	
	
	#Respone comes as unicode,
	str_response = str(response)

	#separate received string into individule values
	#Not needed for current simulations but will be needed in the future
	split_response = str_response.split()
	
	print(split_response[0])
        print(split_response[1])
	

	if ((split_response[0] != '41') and (split_response[1] != '01')):
		#invalid relpy
		print("Invalid reply after first message")
		sys.exit(0)

	 #case for 0 codes
         #case for codes but no light


	intErrorCode = int(split_response[3], 16)
	if intErrorCode < 0x80:
		#Check Engine Lamp or MIL is not on
		nErrorCodes = split_response[3]	
	else:
		#lights are on
        	nErrorCodes = intErrorCode - 0x80

	#Find Actual trouble codes
	#Send mode switch command

	####
	# > 03
	####

	prev_response = response
        client.loop()
        publish(client, "03")
	while response == prev_response:
                time.sleep(.1)
                client.loop()
	str_response = str(response)

	#possible response:
	#43 01 33 00 00 00 00
	# 43 says its a mode 3 response,
	# Next 6 bytes are read in pairs,
	# 0133 0000 0000
	#by standard it is padded with 0s, 0000 do not represent trouble codes
	
	str_response = str_response.split()
	if str_response[0] != "43"
	        print("invalid response")
	        sys.exit(0)
	str_response.pop(0)
	refined_response = [str_response[0] + str_response[1], str_response[2] + str_response[3], str_response[4] + str_response[5]]
	refined_response = [i for i in refined_response if i != "0000"]	


	DTC_dict = { 
		0x0:"P0",
		0x1:"P1",
		0x2:"P2",
		0x3:"P3",
		0x4:"C0",
		0x5:"C1",
		0x6:"C2",
		0x7:"C3",
		0x8:"B0",
		0x9:"B1",
		0xA:"B2",
		0xB:"B3",
		0xC:"U0",
		0xD:"U1",
		0xE:"U2",
		0xF:"U3"}
	
			
	parsedDTC = "Test Dat" 
	rawDTC = "Test Dat"
	

	#export into SQL
	try:
	        sqlcon = sqlite3.connect("data.db")
	        cursor = sqlcon.cursor()
	        #insert collected data into the sqlite3 string
	        insertdata = "insert into data(parsedData, rawData, time) values (\"{}\", \"{}\", \"{}\")".format("test", "Test", datetime.now())
	        count = cursor.execute(insertdata)
	        sqlcon.commit()
	        cursor.close()
	#Error checking
	except sqlite3.Error as error:
	        print("ERROR, ", error)
	
	finally:
	        if sqlcon:
	                sqlcon.close()





























		
	
 
