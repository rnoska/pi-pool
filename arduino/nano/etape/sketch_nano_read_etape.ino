#define FX_READ_ETAPE 48
#define FX_VER        118

int analog_eTape = 0;
int incoming=0;
char* ver="0.1";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  //Serial.print("Started v");
  //Serial.println(ver);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incoming = Serial.read();
    if ( incoming == FX_READ_ETAPE ) {
        Serial.print("received;cmd=48d,fx=readETape,ret=");
        int val=readETape();
        Serial.print(val);  
    } else if ( incoming == FX_VER) {
        Serial.print("received;cmd=");
        Serial.print(FX_VER,DEC);
        Serial.print("d,fx=version,ret=");
        Serial.print(ver);
    } else {
      Serial.print("received;cmd=");
      Serial.print(incoming,DEC);
      Serial.print("d,ret=bad_command");
    }
  }
}
int readETape(){
    int val = analogRead(analog_eTape);    // read the ETape analog input pin
    return val; 
}