import time
import random
from paho.mqtt import client as mqtt

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


def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def publish(client):
    msg_count = 0
    while msg_count < 10:
        time.sleep(1)
        #msg = "messages: %d" % msg_count
        msg = input("Type: ")
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print("Send `%s` to topic `%s`" % (msg, topic))
        else:
            print("Failed to send message to topic %s" % topic)
        msg_count += 1
    #subscribe(client)
    #client.loop_forever()


def run():
    client = connect_mqtt()
    #subscribe(client)
    #i = 0
    #while i < 10:
    #    client.loop()
    #    i = i + 1
    publish(client)
    client.loop_forever()
    #client.loop_forever()


if __name__ == "__main__":
    run()
                                                                                                    69,9          Bot
