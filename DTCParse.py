#!/usr/bin/python3
import mqtt as m
import sys
import random
import re
import time
import sqlite3
from datetime import datetime

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

def log(text):
	#open log file with appened
	f = open("log.txt", "a")
	f.write(str(datetime.now())+ "\t"  + text + "\n")


#Returns a string containing up to 3 error codes
def detectDTC(client):

	#global message_flag to indicate a new message
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



	#Send Mode 1 PID 01 requset
	# >01 01
	#Typical Response:
	#41 01 81 07 65 04

	client.loop()
	#setup abillity to receive messages
	m.subscribe(client, "OBDIIRec")
	
	#send "01 01" message to "OBDIISend2" topic
	m.publish(client, "OBDIISend2", "01 01")
	
	#wait for a new MQTT reply
	while (not message_flag):
		client.loop()
	#reset global flag
	message_flag = False

	#Respone comes as unicode,
	str_response = str(vol_response)
	#separate received string into individule values
	split_response = str_response.split()
	
	if((len(split_response) < 4)):
                #invalid relpy
                #print("Invalid reply after first message")
                log("Invalid reply to 01 01 in DTCParse.py: " + str(split_response))
                print("Invalid reply to 01 01 in DTCParse.py: " + str(split_response))
                #sys.exit(0)
                return "Error occured, please check the log.txt"


	if ((split_response[2] != '41') and (split_response[3] != '01')):
		#invalid relpy
		#print("Invalid reply after first message")
		log("Invalid reply to 01 01 in DTCParse.py: " + str(split_response))
		print("Invalid reply to 01 01 in DTCParse.py: " + str(split_response))
		#sys.exit(0)
		return "Error occured, please check the log.txt"		

	# if the 4th byte is "00" then there are no error codes
	if(split_response[4] == '00'):
		sql_export("No Error Codes")
		return "No Error Codes"

	#if the 4th byte is not zero, convert it into decimal
	intErrorCode = int(split_response[3], 16)
	
	#most significant bit is a 1 if the check engine light is on
	if intErrorCode < 0x80:
		#Check Engine Lamp or MIL is not on,
		#number of error codes is the 4th byte
		nErrorCodes = split_response[3]	
	else:
		#check engine light is on
		#4th byte - 0x80 is the number of error codes
        	nErrorCodes = intErrorCode - 0x80

	#Find Actual trouble codes
	client.loop()
	#send 03 to Remote system to switch ELM327 Modes
	m.publish(client, "OBDIISend2", '03')
	#wait for new MQTT message
	while (not message_flag):
                client.loop()
	message_flag = False
	str_response = vol_response

	print(str_response )
	print(type(str_response))

	str_response = str_response + " 00" + " 00"
	
	#possible response:
	#43 01 33 00 00 00 00
	
	#error check, 43 indicates a response in mode 3
	str_response = str_response.split()	
	if str_response[1] != '43':
	        #log the error
		log("Invalid reply to 03 in DTCParse.py: " + str(str_response))
		print("Invalid reply to 03 in DTCParse.py: " + str(str_response))
		#sys.exit(0)
		return "Error occured, please check the log.txt"
	
	# Next 6 bytes are read in pairs,
        # Ex: 0133 0000 0000
        #by standard it is padded with 0s, 0000 does not represent trouble codes
	str_response.pop(0) # remove the first value, it is just used for confirmation
	
	#convert remeaining bytes to two byte pairs
	refined_response = [str_response[0] + str_response[1], str_response[2] + str_response[3], str_response[4] + str_response[5]]
	#clear out any 0000 codes
	refined_response = [i for i in refined_response if i != "0000"]	

	#first number represents a 2 char value, 
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
	
	#bytes of the return values are combined and decoded using the DTC_dict, values found
	# in ELM327 data sheet
	#array to hold final code values
	parsedDTC = []
	for i in range(len(refined_response)): 
		parsedDTC.append(DTC_dict[refined_response[i][0]] + refined_response[i][1:])	

	#combine codes into 1 string
	combined_DTC = ""
	for i in parsedDTC:
		combined_DTC = combined_DTC + "\t" + str(i)
	#export codes to SQL db	
	sql_export(combined_DTC)
	return combined_DTC	


def clearDTC(client):	
	#global message_flag to indicate a new message
        global message_flag
        message_flag = False
        #define the on_message callback function
        def on_message(client, userdata, msg):
                message = "%s" % msg.payload.decode()
                global vol_response
                global message_flag
                message_flag = True
                vol_response = message
	#set the callback function
        client.on_message = on_message
        m.subscribe(client, "OBDIIRec")
	
	#sending a "04" to the ELM instructs it to clear error codes per the ELM327 datasheet
        m.publish(client, "OBDIISend2", "04")
	
	#wait for a new message	
        while (not message_flag):
                client.loop()
	#reset global message flag
        message_flag = False
        response = (vol_response).split()
        #0x44 is a confirmation that codes were cleared
        if(response[1] != '44'):
                log("Invalid reply to 04 in clearDTC.py: " + str(response))
                print("Invalid reply to 04 in clearDTC.py: " + str(response))
        else:
                log("Codes have been successfully cleared")
                print("Codes have been successfully cleared")





		
	
 
