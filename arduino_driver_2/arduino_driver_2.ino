#include <Servo.h>
#define esc_pin 2
#define servo_pin 3

Servo ESC;
Servo servo;

int drive_mode = 0;		// 0 for capture mode, 1 for control mode
int capture_rate = 10;		// rate at which samples are sent to RPi
float capture_delay = 100;	// delay [ms] of capture loop
char data_in[8];

int esc_pulse = 1500;
int servo_pulse = 1500;
void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(10000);
  pinMode(esc_pin, INPUT);
  pinMode(servo_pin, INPUT);
  //ESC.attach(esc_pin);
  //servo.attach(servo_pin);


  // initialize servo and ESC
  //ESC.writeMicroseconds(1500);
  //servo.writeMicroseconds(1500);
  //delay(3000);


}

void loop()
{
  Serial.readBytes(data_in, 8);
  switch (data_in[0]) {
  case '0':
    // capture mode
      // get inputs
      esc_pulse = pulseIn(esc_pin, HIGH);
      servo_pulse = pulseIn(servo_pin, HIGH);
      //esc_pulse = 1111;
      //servo_pulse = 2222;
      
      Serial.println(String(esc_pulse) + ":" + String(servo_pulse));		
      
    break;
  case '1':
    // control mode
    while(1) {
      Serial.readBytes(data_in, 8);
      esc_pulse = 1000 * (data_in[0] - 48) + 100 * (data_in[1] - 48) + 10 * (data_in[2] - 48) + (data_in[3] - 48);
      servo_pulse = 1000 * (data_in[4] - 48) + 100 * (data_in[5] - 48) + 10 * (data_in[6] - 48) + (data_in[7] - 48);

      ESC.writeMicroseconds(esc_pulse);
      servo.writeMicroseconds(servo_pulse);
      // is this delay necessary??
      delay(10);
    }
    break;
  default:

    break;
  }		
}



