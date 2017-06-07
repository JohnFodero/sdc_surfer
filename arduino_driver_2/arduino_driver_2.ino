#include <Servo.h>
#define esc_pin 2
#define servo_pin 3

Servo ESC;
Servo servo;

int mode = 0;		      // 0 for capture mode, 1 for control mode
char data_in[8];

int esc_pulse = 1500;
int servo_pulse = 1500;
void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(10000);
  Serial.readBytes(data_in, 8);
  switch (data_in[0]) {
  case '0':
    pinMode(esc_pin, INPUT);
    pinMode(servo_pin, INPUT);
    Serial.println('00000000');
    mode = 0;
    break;
  case '1':
    // drive mode
    pinMode(esc_pin, OUTPUT);
    pinMode(servo_pin, OUTPUT);
    ESC.attach(esc_pin);
    servo.attach(servo_pin);
    ESC.writeMicroseconds(1500);
    servo.writeMicroseconds(1500);
    delay(1000);    // ensure ESC is initialized properly
    servo.writeMicroseconds(1400);
    delay(500);
    servo.writeMicroseconds(1600);
    delay(500);
    servo.writeMicroseconds(1500);
    Serial.println("11111111");
    mode = 1;
    break; 
  }


}

void loop()
{
  switch (mode) {
  case 0:
  while(1) {
    // capture mode
    // get inputs
    Serial.readBytes(data_in, 8);
    esc_pulse = pulseIn(esc_pin, HIGH);
    servo_pulse = pulseIn(servo_pin, HIGH);

    Serial.println(String(esc_pulse) + ":" + String(servo_pulse));		
  }
    break;
  case 1:
    // control mode
      while(1) {
      if(Serial.readBytes(data_in, 8) > 0) {
        esc_pulse = 1000 * (data_in[0] - 48) + 100 * (data_in[1] - 48) + 10 * (data_in[2] - 48) + (data_in[3] - 48);
        servo_pulse = 1000 * (data_in[4] - 48) + 100 * (data_in[5] - 48) + 10 * (data_in[6] - 48) + (data_in[7] - 48);
        if(esc_pulse > 1400 && esc_pulse < 1600) {
          ESC.writeMicroseconds(esc_pulse);
          servo.writeMicroseconds(servo_pulse);
        }
        // confirmation
        Serial.println('1');
      }
      else {
        ESC.writeMicroseconds(1500);
        servo.writeMicroseconds(1500);
        Serial.println('0');
      }
    }
    break;
  }		
}






