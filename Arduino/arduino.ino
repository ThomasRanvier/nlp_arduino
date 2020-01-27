#include <Servo.h>

int val = 0;
int ledR = 13; // Led Verte quand bon password
int ledW = 12; // Led Rouge quand mauvais
int ledMDP = 9; // Led quand mot de passe changé
int ledE = 3; // Led quand ecoute
bool newMdp = false; // Variable si mot de passe change
int re = 0;
bool button = false;
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
  if(val == 1 && button == false){
      button = true;
      Serial.print('A');
      digitalWrite(ledE, HIGH);
  }
  if(Serial.available() > 0){
    re = Serial.read();
    digitalWrite(ledE, LOW);
    if(re == 'B'){ // Si bon password
      button = false;
      newMdp = false;
      servo.write(0);
      digitalWrite(ledR, HIGH);
      servo.write(180);
      delay(3000);
      servo.write(0);
      digitalWrite(ledR, LOW);
   }
   if(re == 'C'){ // Si changement de password
     newMdp = true;
   }
   if(re == 'N'){ // si mauvais password
      button = false;
      digitalWrite(ledW, HIGH);
      delay(3000);
      digitalWrite(ledW, LOW);
   }
  }
  if(newMdp){
    delay(200);
    digitalWrite(ledMDP, HIGH);
    delay(200);
    digitalWrite(ledMDP, LOW);
  }
}
