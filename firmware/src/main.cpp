#include <ESP8266React.h>
#include <Scout.h>

#include <ESPAsyncWebServer.h>
#include <Adafruit_PWMServoDriver.h>

#define SERIAL_BAUD_RATE 115200

AsyncWebServer server(80);

ESP8266React esp8266React(&server);
Scout scout(&server, &SPIFFS, esp8266React.getSecurityManager());

void setup() {
    Serial.begin(SERIAL_BAUD_RATE);
    #ifdef ESP32
        SPIFFS.begin(true);
    #elif defined(ESP8266)
        SPIFFS.begin();
    #endif
    esp8266React.begin();
    server.begin();
    scout.begin();
}

void loop() {
  esp8266React.loop();
  scout.loop();
}
