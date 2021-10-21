#include <ESP8266WiFi.h>

const char* ssid = "Foglio2.4"; //Wifi Name
const char* password = "writerheight285";//Wifi password

// MQTT Broker
const char *mqtt_broker = "broker.mqtt-dashboard.com";
const char *topic = "OBDIIRec";
const char *mqtt_username = "XXXXX";
const char *mqtt_password = "public";
const int mqtt_port = 1883;


void setup_wifi() {
  delay(10);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  digitalWrite(LED_BUILTIN, LOW);
}

int setup_Serial() {

  
}

void setup_MQTT() {
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  
}

void callback(char* topic, byte* payload, unsigned int length) {

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
  setup_wifi();
  
}


#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;
void loop(void) {
  if (!client.connected()) {
    reconnect();
  }
  
  client.loop();
  snprintf (msg, MSG_BUFFER_SIZE, "Test: #%d", value);
  client.publish("OBDIIRec", msg);
  value++;
  delay(1000);
}
  
