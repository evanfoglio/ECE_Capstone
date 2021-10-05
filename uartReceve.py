#!/usr/bin/python
import serial
from time import sleep

ser = serial.Serial ("/dev/ttyS0", 115200)    #Open port with baud rate
data = "No Data"
while True:
	
	received_data = ser.read()              #read serial port
	print(received_data)
	if received_data == '<':
		data = received_data
		while received_data != '>':
			data = data + ser.read()
	print (data)
