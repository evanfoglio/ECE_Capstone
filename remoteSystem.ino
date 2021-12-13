#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define MSG_BUFFER_SIZE  50

//initialize global string, this must be global so the callback 
//interupt function and the main loop can have it in their scope
char glob_message[MSG_BUFFER_SIZE] = "Initial Value";

//Wifi Credentials
const char* ssid = "Foglio2.4"; //Wifi Name
const char* password = "writerheight285";//Wifi password
//const char* ssid = "Evans iphone";
//const char* password = "12345678";


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

//initializes MQTT server, however it will not connect until the
//reconnect function is run in the main loop.
void setup_MQTT() {
  client.setServer(mqtt_broker, mqtt_port);  
}

boolean message_flag = false;
void callback(char* topic, byte* payload, unsigned int msg_length) {
  //When a MQTT message comes in, the gobal message variable is cleared out
  memset(glob_message, 0, sizeof glob_message);
  //Global message staores the most recent MQTT message
  //Coppies 1 char at a time
  for (int i = 0; i < msg_length; i++) {
      glob_message[i] = (char) payload[i];
  }
  message_flag = true;
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      // Once connected, publish an announcement
      //HERE IS WHAT HAPPENS IF WE RECONNECT
    } else {
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void serial_flush(void) {
  if (Serial.available()) {
    while (Serial.available()) Serial.read();
  }
}

void setup() {
  //Set LED on ESP12-S to an output
  pinMode(LED_BUILTIN, OUTPUT); 
  //Start serial communication using 9600 baud
  Serial.begin(9600);
  setup_wifi();
  setup_Serial();
  setup_MQTT();
}




void loop(void) {
//If MQTT client is not connected (First loop it is not) Connect 
  if (!client.connected()) {
    reconnect();
  }
  //Set the callback interupt function and the topic that receives the commands
  client.setCallback(callback);
  client.subscribe("OBDIISend2");

  //ATcommand is used to store the value of the global message so it does not change while it is being used
  char ATcommand[MSG_BUFFER_SIZE];
  
  //used to compare and see if the current global message is a new message.
  String prev_msg = glob_message;

  //Waiting for MQTT message...
  while (!message_flag) {
    delay(100);
    //client.loop() updates the MQTT client
    client.loop();
  }
  message_flag = false

  //remove all serial messages in the buffer
  serial_flush();//the function of Serial.flush was changed in Arduino 1.0 to not actually flush the buffer
  //coppy the global message contents into ATcommand array for printing
  for (int i = 0; i < sizeof glob_message ; i++) {
    ATcommand[i] = glob_message[i];

  }
  //Send the AT command to PCB
  Serial.println(ATcommand);
  
  //Waiting for UART Response
  while (!Serial.available()) {
    delay(10);
  }

  char UART_Response[MSG_BUFFER_SIZE];
  char msg[MSG_BUFFER_SIZE];
  //index is used to count the size of the response
  int index = 0;
  //Reading UART
  while (Serial.available() > 0) {
    delay(10);
    UART_Response[index] = Serial.read();
    index++;
  }
  if (index > 0) { // if there was a response, publish the message
    snprintf (msg, index, UART_Response);
    client.publish("OBDIIRec", msg);
    delay(100);
  }
  //Message published
  client.loop();
}
