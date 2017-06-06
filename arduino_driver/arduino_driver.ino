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
  ESC.attach(esc_pin);
  servo.attach(servo_pin);


  // initialize servo and ESC
  ESC.writeMicroseconds(1500);
  servo.writeMicroseconds(1500);
  delay(3000);

  // get operating mode (0 for capture, 1 for control mode)
  Serial.readBytes(data_in, 8);
  if(data_in[0] == '0') {
    Serial.println("capture mode");
    drive_mode = 0;
    // set pins to INPUT
    pinMode(esc_pin, INPUT);
    pinMode(servo_pin, INPUT);
    // bits 4-7 are the capture rate in Hz
    capture_rate = 1000 * (data_in[4] - 48) + 100 * (data_in[5] - 48) + 10 * (data_in[6] - 48) + (data_in[7] - 48);
    capture_delay = 1000.0 / float(capture_rate);
    Serial.println(capture_delay);
  }
  else if(data_in[0] == '1') {
    Serial.println("drive mode");
    drive_mode = 1;
    // set pins to OUTPUT
    pinMode(esc_pin, OUTPUT);
    pinMode(servo_pin, OUTPUT);
    
    // move wheels
    servo.writeMicroseconds(1800);
    delay(500);
    servo.writeMicroseconds(1200);
    delay(500);
    servo.writeMicroseconds(1500);
  }
  else
  {
    while(1) {
      Serial.println("Invalid mode");
    }
  }
}

void loop()
{
  switch (drive_mode) {
  case 0:
    // capture mode
    while(1) {
      // get inputs
      esc_pulse = pulseIn(esc_pin, HIGH);
      servo_pulse = pulseIn(servo_pin, HIGH);
      //esc_pulse = 1111;
      //servo_pulse = 2222;
      
      Serial.println(String(esc_pulse) + ":" + String(servo_pulse));		
      // - 30 to compensate for 20 ms each pulseIn read
      delay(capture_delay - 40);
    }
    break;
  case 1:
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



