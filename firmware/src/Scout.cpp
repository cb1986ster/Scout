#include <Scout.h>


StateUpdateResult ScoutSettings::update(JsonObject& root, ScoutSettings& settings) {
    // 123, 532
    settings.min_00 = root["min_00"] | 140; settings.max_00 = root["max_00"] | 580; settings.pin_00 = root["pin_00"] | 5;
    settings.min_01 = root["min_01"] | 562; settings.max_01 = root["max_01"] | 122; settings.pin_01 = root["pin_01"] | 4;
    settings.min_02 = root["min_02"] | 120; settings.max_02 = root["max_02"] | 540; settings.pin_02 = root["pin_02"] | 3;
    settings.min_03 = root["min_03"] | 120; settings.max_03 = root["max_03"] | 530; settings.pin_03 = root["pin_03"] | 2;
    settings.min_04 = root["min_04"] | 135; settings.max_04 = root["max_04"] | 620; settings.pin_04 = root["pin_04"] | 1;
    settings.min_05 = root["min_05"] | 515; settings.max_05 = root["max_05"] | 110; settings.pin_05 = root["pin_05"] | 0;
    settings.min_06 = root["min_06"] | 110; settings.max_06 = root["max_06"] | 543; settings.pin_06 = root["pin_06"] | 13;
    settings.min_07 = root["min_07"] | 580; settings.max_07 = root["max_07"] | 118; settings.pin_07 = root["pin_07"] | 14;
    settings.min_08 = root["min_08"] | 113; settings.max_08 = root["max_08"] | 530; settings.pin_08 = root["pin_08"] | 15;
    settings.min_09 = root["min_09"] | 100; settings.max_09 = root["max_09"] | 514; settings.pin_09 = root["pin_09"] | 10;
    settings.min_10 = root["min_10"] | 107; settings.max_10 = root["max_10"] | 525; settings.pin_10 = root["pin_10"] | 11;
    settings.min_11 = root["min_11"] | 560; settings.max_11 = root["max_11"] | 115; settings.pin_11 = root["pin_11"] | 12;
    return StateUpdateResult::CHANGED;
}

void ScoutSettings::read(ScoutSettings& settings, JsonObject& root) {
    root["min_00"] = settings.min_00; root["max_00"] = settings.max_00; root["pin_00"] = settings.pin_00;
    root["min_01"] = settings.min_01; root["max_01"] = settings.max_01; root["pin_01"] = settings.pin_01;
    root["min_02"] = settings.min_02; root["max_02"] = settings.max_02; root["pin_02"] = settings.pin_02;
    root["min_03"] = settings.min_03; root["max_03"] = settings.max_03; root["pin_03"] = settings.pin_03;
    root["min_04"] = settings.min_04; root["max_04"] = settings.max_04; root["pin_04"] = settings.pin_04;
    root["min_05"] = settings.min_05; root["max_05"] = settings.max_05; root["pin_05"] = settings.pin_05;
    root["min_06"] = settings.min_06; root["max_06"] = settings.max_06; root["pin_06"] = settings.pin_06;
    root["min_07"] = settings.min_07; root["max_07"] = settings.max_07; root["pin_07"] = settings.pin_07;
    root["min_08"] = settings.min_08; root["max_08"] = settings.max_08; root["pin_08"] = settings.pin_08;
    root["min_09"] = settings.min_09; root["max_09"] = settings.max_09; root["pin_09"] = settings.pin_09;
    root["min_10"] = settings.min_10; root["max_10"] = settings.max_10; root["pin_10"] = settings.pin_10;
    root["min_11"] = settings.min_11; root["max_11"] = settings.max_11; root["pin_11"] = settings.pin_11;
}

Scout::Scout(AsyncWebServer* server, FS* fs, SecurityManager* securityManager) :
    _httpEndpoint(ScoutSettings::read,
                  ScoutSettings::update,
                  this,
                  server,
                  SCOUT_SETTINGS_PATH,
                  securityManager,
                  AuthenticationPredicates::IS_AUTHENTICATED),
    _fsPersistence(ScoutSettings::read, ScoutSettings::update, this, fs, SCOUT_SETTINGS_FILE) {
};

void Scout::begin() {
  pwm.begin();
  pwm.setPWMFreq(50);
  _fsPersistence.readFromFS();
  freqs[0] = _state.min_00 + ((_state.max_00-_state.min_00)/2);
  freqs[1] = _state.min_01 + ((_state.max_01-_state.min_01)/2);
  freqs[2] = _state.min_02 + ((_state.max_02-_state.min_02)/2);
  freqs[3] = _state.min_03 + ((_state.max_03-_state.min_03)/2);
  freqs[4] = _state.min_04 + ((_state.max_04-_state.min_04)/2);
  freqs[5] = _state.min_05 + ((_state.max_05-_state.min_05)/2);
  freqs[6] = _state.min_06 + ((_state.max_06-_state.min_06)/2);
  freqs[7] = _state.min_07 + ((_state.max_07-_state.min_07)/2);
  freqs[8] = _state.min_08 + ((_state.max_08-_state.min_08)/2);
  freqs[9] = _state.min_09 + ((_state.max_09-_state.min_09)/2);
  freqs[10] = _state.min_10 + ((_state.max_10-_state.min_10)/2);
  freqs[11] = _state.min_11 + ((_state.max_11-_state.min_11)/2);
  StreamUdp.begin(UDP_PORT);
  pinMode(LED_BUILTIN, OUTPUT);
  delay(500);
};

void Scout::servoOff(){
    pwm.setPWM(_state.pin_00, 0, 0); pwm.setPWM(_state.pin_01, 0, 0); pwm.setPWM(_state.pin_02, 0, 0);
    pwm.setPWM(_state.pin_03, 0, 0); pwm.setPWM(_state.pin_04, 0, 0); pwm.setPWM(_state.pin_05, 0, 0);
    pwm.setPWM(_state.pin_06, 0, 0); pwm.setPWM(_state.pin_07, 0, 0); pwm.setPWM(_state.pin_08, 0, 0);
    pwm.setPWM(_state.pin_09, 0, 0); pwm.setPWM(_state.pin_10, 0, 0); pwm.setPWM(_state.pin_11, 0, 0);
};
void Scout::servoUpdate(){
    pwm.setPWM(_state.pin_00, 0, freqs[0]);pwm.setPWM(_state.pin_01, 0, freqs[1]);pwm.setPWM(_state.pin_02, 0, freqs[2]);
    pwm.setPWM(_state.pin_03, 0, freqs[3]);pwm.setPWM(_state.pin_04, 0, freqs[4]);pwm.setPWM(_state.pin_05, 0, freqs[5]);
    pwm.setPWM(_state.pin_06, 0, freqs[6]);pwm.setPWM(_state.pin_07, 0, freqs[7]);pwm.setPWM(_state.pin_08, 0, freqs[8]);
    pwm.setPWM(_state.pin_09, 0, freqs[9]);pwm.setPWM(_state.pin_10, 0, freqs[10]);pwm.setPWM(_state.pin_11, 0, freqs[11]);
};

void Scout::loop() {
    static unsigned char buff[2048];
    static uint32_t len,*ti;
    static float *tf;

    if(millis()%200 > 100) digitalWrite(LED_BUILTIN, HIGH);
    else digitalWrite(LED_BUILTIN, LOW);

    if(StreamUdp.parsePacket()) {
      len = StreamUdp.read(buff, 2048);
      if (len > 0){
        switch(buff[0]){
            case 'D': servosUp = false; break;
            case 'U': servosUp = true; break;
            case 'A':
                tf = (float*)(buff+1);
                freqs[0] = _state.min_00 + ((tf[0]+1)*(_state.max_00-_state.min_00)/2);
                freqs[1] = _state.min_01 + ((tf[1]+1)*(_state.max_01-_state.min_01)/2);
                freqs[2] = _state.min_02 + ((tf[2]+1)*(_state.max_02-_state.min_02)/2);
                freqs[3] = _state.min_03 + ((tf[3]+1)*(_state.max_03-_state.min_03)/2);
                freqs[4] = _state.min_04 + ((tf[4]+1)*(_state.max_04-_state.min_04)/2);
                freqs[5] = _state.min_05 + ((tf[5]+1)*(_state.max_05-_state.min_05)/2);
                freqs[6] = _state.min_06 + ((tf[6]+1)*(_state.max_06-_state.min_06)/2);
                freqs[7] = _state.min_07 + ((tf[7]+1)*(_state.max_07-_state.min_07)/2);
                freqs[8] = _state.min_08 + ((tf[8]+1)*(_state.max_08-_state.min_08)/2);
                freqs[9] = _state.min_09 + ((tf[9]+1)*(_state.max_09-_state.min_09)/2);
                freqs[10] = _state.min_10 + ((tf[10]+1)*(_state.max_10-_state.min_10)/2);
                freqs[11] = _state.min_11 + ((tf[11]+1)*(_state.max_11-_state.min_11)/2);
                break;
            case 'F':
                ti = (uint32_t*)(buff+1);
                freqs[0] = ti[0];
                freqs[1] = ti[1];
                freqs[2] = ti[2];
                freqs[3] = ti[3];
                freqs[4] = ti[4];
                freqs[5] = ti[5];
                freqs[6] = ti[6];
                freqs[7] = ti[7];
                freqs[8] = ti[8];
                freqs[9] = ti[9];
                freqs[10] = ti[10];
                freqs[11] = ti[11];
                break;
        }
      }
    }
    if(servosUp)servoUpdate(); else servoOff();
};
