#include <Servo.h>
#define esc_pin 2
#define servo_pin 3
#define th_pin 4
#define st_pin 5
#define SENSITIVITY 10
Servo ESC;
Servo servo;

int mode = 0;		      // 0 for capture mode, 1 for control mode
char data_in[8];
bool initializing = true;
int st;
int th;
int sv = 1500, prev_sv = 1500;
int esc = 1500, prev_esc = 1500;
void setup()
{

  Serial.begin(115200);
  Serial.setTimeout(1000);

  pinMode(esc_pin, OUTPUT);
  pinMode(servo_pin, OUTPUT);
  pinMode(th_pin, INPUT);
  pinMode(st_pin, INPUT);
  ESC.attach(esc_pin);
  servo.attach(servo_pin);
  ESC.writeMicroseconds(1500);
  servo.writeMicroseconds(1500);
  delay(1000);    // ensure ESC is initialized properly

  while(initializing) {
    Serial.readBytes(data_in, 8);
    if(data_in[0] == '0') {
      Serial.println("00000000");
      mode = 0;
      initializing = false;
    }
    else if(data_in[0] == '1') {
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
        th = pulseIn(th_pin, HIGH);
        st = pulseIn(st_pin, HIGH);
        prev_esc = esc;
        prev_sv = sv;
        esc = map(th, 855, 1724, 1000, 2000);
        sv = map(st, 855, 1724, 1000, 2000);
        //esc = smooth_output(esc, prev_esc);
        //sv = smooth_output(sv, prev_sv);
       
        ESC.writeMicroseconds(esc);
        servo.writeMicroseconds(sv);
        if(Serial.read() == '0') {
          Serial.println(String(esc) + ":" + String(sv));
        }
      }
    break;
    case 1:
      Serial.setTimeout(500);
      while(true) {
        if(Serial.readBytes(data_in, 8) >= 8) {
          esc = 1000 * (data_in[0] - 48) + 100 * (data_in[1] - 48) + 10 * (data_in[2] - 48) + (data_in[3] - 48);
          sv = 1000 * (data_in[4] - 48) + 100 * (data_in[5] - 48) + 10 * (data_in[6] - 48) + (data_in[7] - 48);
          ESC.writeMicroseconds(esc);
          servo.writeMicroseconds(sv);
          Serial.println("1");
        }
        else {
          // failsafe: if not enough serial data is received, stop esc and center servo
          ESC.writeMicroseconds(1500);
          servo.writeMicroseconds(1500);
          Serial.println("0");
        }
      }
    break;
  }


}


int smooth_output(int val, int prev_val) {
  int confidence = (val - prev_val) * (val - prev_val);
  if (confidence > SENSITIVITY) {
    return val;
  }
  else {
    return prev_val;
  }
}






