#define RELAY1 7
#define RELAY2 8

void setup() {
  Serial.begin(9600);

  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);

  digitalWrite(RELAY1, LOW);
  digitalWrite(RELAY2, LOW);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "ON") {
      digitalWrite(RELAY1, HIGH);
      digitalWrite(RELAY2, HIGH);
      Serial.println("ALL RELAYS ON");
    }

    else if (cmd == "OFF") {
      digitalWrite(RELAY1, LOW);
      digitalWrite(RELAY2, LOW);
      Serial.println("ALL RELAYS OFF");
    }
  }
}
