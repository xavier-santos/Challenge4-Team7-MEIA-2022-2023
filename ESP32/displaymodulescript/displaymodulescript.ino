#include <WiFi.h>
#include <PubSubClient.h>
#include "SevSeg.h"

const char* ssid = "iPhone de Xavier (2)";
const char* password = "pequena132";
const char* mqttServer = "172.20.10.6";
const int mqttPort = 1883;
const char* mqttTopic = "pz1_display_value";

WiFiClient espClient;
PubSubClient client(espClient);
SevSeg sevseg;

void setup() {
  // Connect to Wi-Fi
  Serial.begin(115200);
  Serial.println("IM ALIVE");
  WiFi.mode(WIFI_STA); // Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }
  Serial.println("WiFi connected");

  IPAddress ip;
  if (WiFi.hostByName(mqttServer, ip)) {
    Serial.print("Ping successful. IP address: ");
    Serial.println(ip);
  } else {
    Serial.println("Ping failed");
  }

  // Connect to MQTT Broker
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  
  // Initialize the seven-segment display
  byte sevenSegments = 1;
  byte CommonPins[] = {};
  byte LEDsegmentPins[] = {13, 12, 14, 27, 26, 25, 33};
  bool resistorsOnSegments = true;
  sevseg.begin(COMMON_ANODE, sevenSegments, CommonPins, LEDsegmentPins, resistorsOnSegments);
  sevseg.setBrightness(80);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
} 

void callback(char* topic, byte* payload, unsigned int length) {
  // Convert the received payload to a string
  payload[length] = '\0';
  String message = String((char*)payload);
  
  // Check if the received topic matches the subscribed topic
  if (String(topic) == mqttTopic) {
    // Update the display with the received value
    int value = message.toInt();
    Serial.println(message);
    sevseg.setNumber(value);
    sevseg.refreshDisplay();
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe(mqttTopic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}