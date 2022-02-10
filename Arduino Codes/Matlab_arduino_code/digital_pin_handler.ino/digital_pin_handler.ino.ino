int Pin;
int on;
String raw;
String raw1;
String raw2;

void setup() {
  Serial.begin(9600);
  Serial.println("Connected to Bioarma");
}


void loop() {
    byte numByteAvailable = Serial.available();
    if (numByteAvailable >= 1) {
        raw = Serial.readString();
        raw2 = raw.substring(0, 1);
        raw1 = raw.substring(1, 3);
        Pin = raw1.toInt();
        on = raw2.toInt();
        
        if(Pin)
        {
          pinMode(Pin, OUTPUT);
          if(on){
            digitalWrite(Pin, HIGH);
          }
          else{
             digitalWrite(Pin, LOW);
            };
        };
    };

    
    
}
