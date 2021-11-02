#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define MSG_BUFFER_SIZE  50

//initialize global string, this must be global so the callback 
//interupt function and the main loop can have it in their scope
char glob_message[MSG_BUFFER_SIZE] = "Initial Value";

//Wifi Credentials
const char* ssid = "Foglio2.4"; //Wifi Name
const char* password = "writerheight285";//Wifi password

// MQTT Broker
const char *mqtt_broker = "broker.mqtt-dashboard.com";
const char *topic = "OBDIIRec";
const char *mqtt_username = "XXXXX";
const char *mqtt_password = "public";
const int mqtt_port = 1883;


WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  //Make sure LED is off
  digitalWrite(LED_BUILTIN, HIGH);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  //wait for wifi to connect
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
	//LED turns on when wifi is connected
  digitalWrite(LED_BUILTIN, LOW);
}


void setup_MQTT() {
  client.setServer(mqtt_broker, mqtt_port);  
}


void callback(char* topic, byte* payload, unsigned int length) {
  glob_message = "";
  for (int i = 0; i < length; i++) {
      glob_message[i] = (char) payload[i];
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      // Once connected, publish an announcement...
      //HERE IS WHAT HAPPENS IF WE RECONNECT
    } else {
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void setup() {
  pinMode(LED_BUILTIN, OUTPUT); 
  Serial.begin(9600)
  setup_wifi();
  setup_Serial();
  setup_MQTT();
}




void loop(void) {
  if (!client.connected()) {
    reconnect();
  }
  if (!client.connected()) {
    reconnect();
  }
  client.setCallback(callback);
  client.subscribe("OBDIISend");  

  char x[50];
  int index = 0;
  //Read UART input
  while(Serial.available() > 0) {
    x[index] = Serial.read();
    index++;
  }
  if(index > 0) {
    snprintf (msg, index, x);
    client.publish("OBDIIRec", msg);
    delay(1000);
  }
  delay(500);
  client.loop();
}
  
