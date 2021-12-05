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

def log(text):
        #open log file with appened
        f = open("log.txt", "a")
        f.write(str(datetime.now())+ "\t"  + text + "\n")


message_flag = False
def on_message(client, userdata, msg):
	message = "%s" % msg.payload.decode()
	global vol_response
	global message_flag
	vol_response = message
	message_flag = True

m.subscribe(client, "OBDIIRec")
client.on_message = on_message

m.publish(client, "OBDIISend2", "04")

while (not message_flag):
	time.sleep(.1)
	client.loop()
message_flag = False



response = (str(vol_response)).split()
if(response[1] != '44'):
	log("Invalid reply to 04 in clearDTC.py: " + str(response))
	print("Invalid reply to 04 in clearDTC.py: " + str(response))
else:
	log("Codes have been successfully cleared")
	print("Codes have been successfully cleared")


