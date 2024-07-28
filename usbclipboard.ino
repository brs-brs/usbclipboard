#include <Keyboard.h>
#include <EEPROM.h>

const int ledPin = LED_BUILTIN;
const int maxPwdLength = 50;

String PWD = "";

void setup() {
  pinMode(ledPin, OUTPUT);

  PWD = readPWDFromEEPROM();
  if (PWD.length() > 0) {
    digitalWrite(ledPin, HIGH);
    typePWD(PWD);
    clearPWDFromEEPROM();
  }
  else {
    digitalWrite(ledPin, LOW);
  }
  Serial.begin(9600);
}

void loop() {
  while (!Serial) {
    ;
  }
  while (Serial.available() == 0) {
    ;
  }
  PWD = Serial.readStringUntil('\n');
  if (PWD.length() > 0) {
      if (PWD == "######CLIP?######") { 
        // handshake reply
        Serial.write("board");
      } 
      else {
          writePWDToEEPROM(PWD);
          digitalWrite(ledPin, HIGH);
          // ACK
          Serial.write("gotit");
      }
  }
}

void writePWDToEEPROM(String pwd) {
  for (int i = 0; i < maxPwdLength; i++) {
    if (i < pwd.length()) {
      EEPROM.write(i, pwd[i]);
    } else {
      EEPROM.write(i, 0); // Write null terminator
    }
  }
}

String readPWDFromEEPROM() {
  String pwd = "";
  for (int i = 0; i < maxPwdLength; i++) {
    char c = EEPROM.read(i);
    if (c == 0) break; // Stop reading at null terminator
    pwd += c;
  }
  return pwd;
}

void clearPWDFromEEPROM() {
  for (int i = 0; i < maxPwdLength; i++) {
    EEPROM.write(i, 0);
  }
  digitalWrite(ledPin, LOW);
}

void typePWD(String pwd) {
  // Serial.end();
  delay(200);
  Keyboard.begin();
  delay(500);
  Keyboard.print(pwd);
  delay(500);
  Keyboard.end(); 
  delay(200);
}
