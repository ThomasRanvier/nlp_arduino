#include <Servo.h>

int val = 0;
int pin = 13;
Servo servo;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT);
  pinMode(pin, OUTPUT);
  servo.attach(7);
}

void loop() {
  val = digitalRead(2);  // read the input pin
  if(val == 1){
      Serial.print('A');
      delay(3000);
  }
  if(Serial.available() > 0){
    if(Serial.read() == 'B'){
      servo.write(0);
      digitalWrite(pin, HIGH);
      servo.write(180);
      delay(3000);
      servo.write(0);
      digitalWrite(pin, LOW);
   }
  }
}
