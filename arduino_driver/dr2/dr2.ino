#include <Servo.h>
#define esc_pin 2
#define servo_pin 3
#define th_pin 4
#define st_pin 5
Servo ESC;
Servo servo;

int mode = 0;		      // 0 for capture mode, 1 for control mode
char data_in[8];

int st;
int th;
int sv;
int esc;
void setup()
{
  pinMode(esc_pin, OUTPUT);
  pinMode(servo_pin, OUTPUT);
  pinMode(th_pin, INPUT);
  pinMode(st_pin, INPUT);
  ESC.attach(esc_pin);
  servo.attach(servo_pin);
  ESC.writeMicroseconds(1500);
  servo.writeMicroseconds(1500);
  delay(1000);    // ensure ESC is initialized properly

  Serial.begin(115200);


}

void loop()
{
  th = pulseIn(th_pin, HIGH);
  st = pulseIn(st_pin, HIGH);
  esc = map(th, 855, 1724, 1000, 2000);
  sv = map(st, 855, 1724, 1000, 2000);
  Serial.println(esc);
  ESC.writeMicroseconds(esc);
  servo.writeMicroseconds(sv);
}









