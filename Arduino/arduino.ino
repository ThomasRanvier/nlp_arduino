#include <Servo.h>

int val = 0;
int ledR = 13; // Led Verte quand bon password
int ledW = 10; // Led Rouge quand mauvais
int ledMDP = 9; // Led quand mot de passe changé
int ledE = 3; // Led quand ecoute
bool newMdp = false; // Variable si mot de passe change
Servo servo;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT);
  pinMode(ledR, OUTPUT);
  pinMode(ledW, OUTPUT);
  pinMode(ledMDP, OUTPUT);
  pinMode(ledE, OUTPUT);
  servo.attach(7);
}

void loop() {
  val = digitalRead(2);  // read the input pin
  if(val == 1){
      Serial.print('A');
      digitalWrite(ledE, HIGH);
      delay(3000);
      digitalWrite(ledE, LOW);
  }
  if(Serial.available() > 0){
    if(Serial.read() == 'B'){ // Si bon password
      newMdp = false;
      servo.write(0);
      digitalWrite(pin, HIGH);
      servo.write(180);
      delay(3000);
      servo.write(0);
      digitalWrite(pin, LOW);
   }else if(Serial.read() == 'C'){ // Si changement de password
     newMdp = true;
   } else if(Serial.read() == 'N'){ // si mauvais password
      digitalWrite(ledW, HIGH);
      delay(3000);
      digitalWrite(ledW, LOW);
   }
  }
  if(newMdp){
    delay(500);
    digitalWrite(ledMDP, HIGH);
    delay(500);
    digitalWrite(ledMDP, LOW);
  }
}
