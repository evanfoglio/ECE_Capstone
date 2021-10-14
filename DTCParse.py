#!/usr/bin/python
import sys
import re
import sqlite3
from datetime import datetime


def errorCheck():
	if len(sys.argv) != 7:
		output = -1
	#	sys.stdout.write('Not enough Args\n')
#		print('Not enough args')
		return -1
		#sys.exit(0)
	else:
		return 1

if __name__ == "__main__":
	
	#Send Mode 1 PID 01 requset
	# >01 01
	#Typical Response:
	#41 01 81 07 65 04
	
	####
	#SEND REQUEST TBD
	####
	
	####
	# RECEIVE RESPONSE TBD
	####
		
	#Simulate received request:
	if(errorCheck() < 0):
		print("Not enough args")
		sys.exit(0)
	
	x = sys.argv
	print(x)

	#separate received string into individule values
	#x = x.split()
	
	x = sys.argv
	if ((x[1] != '41') and (x[2] != '01')):
		#invalid relpy
		print("Invalid reply after first message")
		sys.exit(0)

	 #case for 0 codes
         #case for codes but no light


	intErrorCode = int(x[3], 16)
	if intErrorCode < 0x80:
		#Check Engine Lamp or MIL is not on
		nErrorCodes = x[3]	
	else:
		#lights are on
        	nErrorCodes = intErrorCode - 0x80

	#Find Actual trouble codes
	#Send mode switch command

	####
	# > 03
	####

	#possible response:
	#43 01 33 00 00 00 00
	# 43 says its a mode 3 response,
	# Next 6 bytes are read in pairs,
	# 0133 0000 0000
	#by standard it is padded with 0s, 0000 do not represent trouble codes
	
	#modify string to actually usable
	

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
	
			
	#parsedDTC = 
	#rawDTC = 
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





























		
	
 
