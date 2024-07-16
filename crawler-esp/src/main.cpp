#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "your_ssid";
const char* password = "your_password";

// MQTT broker
const char* mqtt_broker = "your_broker_address";
const char* topic = "car/control";
const char* mqtt_username = "your_mqtt_username";
const char* mqtt_password = "your_mqtt_password";
const int mqtt_port = 1883;

// UART setup
HardwareSerial mySerial(2); // Use UART2

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  // Start serial communication
  Serial.begin(115200);
  mySerial.begin(115200, SERIAL_8N1, 16, 17); // RX = GPIO16, TX = GPIO17
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");

  // Connect to MQTT broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP32Client", mqtt_username, mqtt_password)) {
      Serial.println("Connected to MQTT broker");
    } else {
      Serial.print("Failed to connect to MQTT broker, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
  client.subscribe(topic);
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received: ");
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    mySerial.write(payload[i]); // Send received message via UART
  }
  Serial.println();
}

void loop() {
  client.loop();
}
