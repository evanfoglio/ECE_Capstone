#include <ESP8266WiFi.h>

const char* ssid = "Foglio2.4"; //Wifi Name
const char* password = "writerheight285";//Wifi password
broker

int value = 0;

void setup_wifi() {
  delay(10);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

int setup_Serial() {

  
}

void setup_MQTT() {

  
}


void setup() {
 
  setup_wifi();
  
}

void loop(void) {
  
}
  
