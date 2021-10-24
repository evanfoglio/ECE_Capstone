import random
import time
from paho.mqtt import client as mqtt


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
        client.subscribe(topic)

def publish(client, topic, msg):
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status != 0:
                print("Failed to send message")


