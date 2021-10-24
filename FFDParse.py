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
response = "init"

client = m.connect_mqtt(client_id, broker, port, username, password)
time.sleep(3)


if __name__ == "__main__":
	
	if len(sys.argv) < 2:
		print("Not Enough Arguments")
