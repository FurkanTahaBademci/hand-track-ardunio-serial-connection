void setup() {
  pinMode(12, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(20000); 
}

void loop() {
  
   if(Serial.available()){ 
    
    char veri = Serial.read();
    if(veri=='0'){ 
      digitalWrite(12, LOW);
      delay(10);
    }
  
    else if(veri=='1'){
      delay(10);
      digitalWrite(12, HIGH);
    }
  }
}
