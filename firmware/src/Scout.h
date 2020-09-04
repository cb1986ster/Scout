#ifndef Scout_h
#define Scout_h

#include <HttpEndpoint.h>
#include <StatefulService.h>
#include <FSPersistence.h>
#include <ESPAsyncWebServer.h>

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#include <WiFiUdp.h>

#define SCOUT_SETTINGS_FILE "/config/scout.json"
#define SCOUT_SETTINGS_PATH "/rest/scout"
#define UDP_PORT 7080

class ScoutSettings {
 public:
    uint16_t min_00; uint16_t max_00; uint16_t pin_00;
    uint16_t min_01; uint16_t max_01; uint16_t pin_01;
    uint16_t min_02; uint16_t max_02; uint16_t pin_02;
    uint16_t min_03; uint16_t max_03; uint16_t pin_03;
    uint16_t min_04; uint16_t max_04; uint16_t pin_04;
    uint16_t min_05; uint16_t max_05; uint16_t pin_05;
    uint16_t min_06; uint16_t max_06; uint16_t pin_06;
    uint16_t min_07; uint16_t max_07; uint16_t pin_07;
    uint16_t min_08; uint16_t max_08; uint16_t pin_08;
    uint16_t min_09; uint16_t max_09; uint16_t pin_09;
    uint16_t min_10; uint16_t max_10; uint16_t pin_10;
    uint16_t min_11; uint16_t max_11; uint16_t pin_11;
  static void read(ScoutSettings& settings, JsonObject& root);
  static StateUpdateResult update(JsonObject& root, ScoutSettings& settings);
};

class Scout : public StatefulService<ScoutSettings> {
    public:
        Scout(AsyncWebServer* server, FS* fs, SecurityManager* securityManager);
        void begin();
        void loop();
    private:
        Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
        WiFiUDP StreamUdp;
        HttpEndpoint<ScoutSettings> _httpEndpoint;
        FSPersistence<ScoutSettings> _fsPersistence;
        void servoOff();
        void servoUpdate();
        uint16_t freqs[12];
        bool servosUp = false;
};

#endif // end Scout_h
