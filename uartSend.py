#!/usr/bin/python
import serial
from time import sleep

ser = serial.Serial ("/dev/serial0", 9600)    #Open port with baud rate
x = "<Hello>"
while True:
	#received_data = ser.read()              #read serial port
	#sleep(0.03)
	#data_left = ser.inWaiting()             #check for remaining byte
	#received_data += ser.read(data_left)
	#print (received_data)
	#ser.write("Hello")                   #print received data
#	x = raw_input()
#	x = "HelloU"
	ser.write(x)
#	sleep(.25)
