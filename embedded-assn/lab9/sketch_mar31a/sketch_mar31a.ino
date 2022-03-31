void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int aread1 = analogRead(A1);
  delay(1);
  int aread2 = analogRead(A2);

  if (aread2 > aread1){
    Serial.println(aread2);
  } else {
    Serial.println("printing Nothing");
  }
}
