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

def on_message(client, userdata, msg):
                message = "%s" % msg.payload.decode()
                global vol_response
                vol_response = message
m.subscribe(client, "OBDIIRec")
client.on_message = on_message

def two_byte_response(cmd):
        #SEND AT 01 cmd
        prev_response = vol_response
        at_cmd = "01 %s" % cmd
        m.publish(client, "OBDIISend2", at_cmd)

        #RECEIVE 41 cmd data
        while vol_response == prev_response:
                time.sleep(.1)
                client.loop()

        response = (str(vol_response)).split()

        if response[2] != '41' and response[3] != cmd:
                #bad response
                print("Invalid response, exiting")
                sys.exit(0)
        else:   #Return 3rd byte
                return [response[4], response[5]]


if __name__ == "__main__":
	

	engine_runtime_bytes = two_byte_response("1F")
	engine_runtime_bytes[0] = int(engine_runtime_bytes[0], 16)
	engine_runtime_bytes[1] = int(engine_runtime_bytes[1], 16)
	engine_runtime = (256 * engine_runtime_bytes[0]) + engine_runtime_bytes[1]

	try:
                sqlcon = sqlite3.connect("engineRuntime.db")
                cursor = sqlcon.cursor()
                #insert collected data into the sqlite3 string
                
		insertdata = "insert into data(Engine_runtime, datetime) values(\"{}\", \"{}\")".format(engine_runtime, datetime.now())
		
		count = cursor.execute(insertdata)
                sqlcon.commit()
                cursor.close()
        #Error checking
        except sqlite3.Error as error:
                print("ERROR, ", error)

        finally:
                if sqlcon:
                        sqlcon.close()
