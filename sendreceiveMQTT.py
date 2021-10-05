#!/usr/bin/python
import time
import random
from paho.mqtt import client as mqtt
from threading import Thread

broker = "broker.emqx.io"
port = 1883
topic = "/python/etest"
randomVal = random.randint(0, 1000)
client_id = "python-mqtt-%d" % randomVal

username = "emqx"
password = "public"

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
		print("Received `%s`" % (msg.payload.decode())) #msg.topic))

	client.subscribe(topic)
	client.on_message = on_message


def publish(client):
	#msg_count = 0
	#while msg_count < 10:
	msg = "XXXX"
	#while True:
	time.sleep(1)
	#msg = "messages: %d" % msg_count
	msg = raw_input("Type: ")
	result = client.publish(topic, msg)
	# result: [0, 1]
	status = result[0]
	if status == 0:
		#print("Send `%s` to topic `%s`" % (msg, topic))
		print("Sent message, topic = %s" % topic)
	else:
		print("Failed to send message to topic %s" % topic)
		#msg_count += 1
	#subscribe(client)
	#client.loop_forever()

def user_input():
	user_input = raw_input()
	return user_input
def thread_one():
	#client = connect_mqtt()
	subscribe(client)
	client.loop_start()

#def thread_two


client = connect_mqtt()
# Main fuction pretty much
def run():
	
	t1 = Thread(target=thread_one)
	#t2 = Thread(target=thread2)
	t1.start()
	time.sleep(1)
	#client = connect_mqtt()
	#client.loop_start()
	#publish(client)
	print("This is like the web thing \n")
	while True :
		x = user_input()	

		if x == 'q' :
			t1.join()
			quit()
			print("Should have quit")

		if x == 'send':
			publish(client)































if __name__ == '__main__':
	run()
