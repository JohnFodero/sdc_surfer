#include <Servo.h>

#define servo_pin 3
#define st_pin 3
#define SENSITIVITY 10

Servo servo;

int mode = 0;		      // 0 for capture mode, 1 for control mode
char data_in[8];
bool initializing = true;
int st;
int th;
int sv = 1500;
int esc = 0000;
void setup()
{

  Serial.begin(115200);
  Serial.setTimeout(1000);

  pinMode(servo_pin, OUTPUT);
  pinMode(st_pin, INPUT);


  while(initializing) {
    Serial.readBytes(data_in, 8);
    if(data_in[0] == '0') {
      Serial.println("00000000");
      mode = 0;
      initializing = false;
    }
    else if(data_in[0] == '1') {
      
      servo.attach(servo_pin);
      servo.writeMicroseconds(1500);
      Serial.println("11111111");
      mode = 1;
      initializing = false;
    }
  }

}

void loop()
{
  switch (mode) {
  case 0:
    Serial.setTimeout(10);
    while(true) {
      st = pulseIn(st_pin, HIGH);
      sv = map(st, 855, 1724, 1000, 2000);

      if(Serial.read() == '0') {
        Serial.println(String(esc) + ":" + String(sv));
      }
    }
    break;
  case 1:
    Serial.setTimeout(500);
    while(true) {
      if(Serial.readBytes(data_in, 8) >= 8) {
        sv = 1000 * (data_in[4] - 48) + 100 * (data_in[5] - 48) + 10 * (data_in[6] - 48) + (data_in[7] - 48);
        servo.writeMicroseconds(sv);
        Serial.println("1");
      }
      else {
        // failsafe: if not enough serial data is received, center servo
        servo.writeMicroseconds(1500);
        Serial.println("0");
      }
    }
    break;
  }


}







