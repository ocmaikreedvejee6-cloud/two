#include <WiFi.h>
#include <WebServer.h>

// ================= WIFI CONFIG =================
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// ================= WEB SERVER =================
WebServer server(80);

// ================= RELAY PINS =================
// Change depending on your ESP32 board wiring
#define RELAY1 12
#define RELAY2 13
#define RELAY3 14

// ================= SETUP =================
void setup() {
  Serial.begin(115200);

  // Set relay pins as output
  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);
  pinMode(RELAY3, OUTPUT);

  // Start OFF (IMPORTANT: depends on relay module, LOW = OFF for most)
  digitalWrite(RELAY1, LOW);
  digitalWrite(RELAY2, LOW);
  digitalWrite(RELAY3, LOW);

  // Connect WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // ================= ROUTES =================

  // ALL RELAYS ON
  server.on("/on", []() {
    digitalWrite(RELAY1, HIGH);
    digitalWrite(RELAY2, HIGH);
    digitalWrite(RELAY3, HIGH);

    server.send(200, "text/plain", "ALL RELAYS ON");
  });

  // ALL RELAYS OFF
  server.on("/off", []() {
    digitalWrite(RELAY1, LOW);
    digitalWrite(RELAY2, LOW);
    digitalWrite(RELAY3, LOW);

    server.send(200, "text/plain", "ALL RELAYS OFF");
  });

  // Start server
  server.begin();
  Serial.println("HTTP server started");
}

// ================= LOOP =================
void loop() {
  server.handleClient();
}
