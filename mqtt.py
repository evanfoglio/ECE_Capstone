import random
import time
from paho.mqtt import client as mqtt


#MQTT#######################################################

def connect_mqtt(client_id, broker, port, username, password):
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

def subscribe(client, topic):
        def on_message(client, userdata, msg):
                message = "%s" % msg.payload.decode()
                global response
                response = message
        client.subscribe(topic)
        client.on_message = on_message

def publish(client, topic, msg):
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status != 0:
                print("Failed to send message")

def waitForResponse(client, topic):
	response = "temp"
	def on_message(client, userdata, msg):
                global response
		response = "%s" % msg.payload.decode()
	client.on_message = on_message
	subscribe(client, topic)
	prev_response = response
	while response == prev_response:
                time.sleep(1)
		print(response)
                client.loop()
	return response



###########################################################

