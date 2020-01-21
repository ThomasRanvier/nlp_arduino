int val = 0;
int pin = 13;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT);
  pinMode(pin, OUTPUT);
}

void loop() {
  val = digitalRead(2);  // read the input pin
  if(val == 1){
      Serial.print('A');
      delay(3000);
  }
  if(Serial.available() > 0){
    if(Serial.read() == 'B'){
      digitalWrite(pin, HIGH);
      delay(2000);
      digitalWrite(pin, LOW);
   }
  }
}
