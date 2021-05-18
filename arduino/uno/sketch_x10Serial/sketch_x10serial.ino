

#include "x10.h"
#include "x10constants.h"

//#define DEBUG
#define X10SEND

// Create array of 10 values for lookup

byte HouseCode[] = { A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P };
byte UnitNum[] = { UNIT_1, UNIT_2, UNIT_3, UNIT_4, UNIT_5, UNIT_6, UNIT_7,
    UNIT_8, UNIT_9, UNIT_10, UNIT_11, UNIT_12, UNIT_13, UNIT_4, UNIT_15,
    UNIT_16 };
byte Cmd[] = { ALL_UNITS_OFF, ALL_LIGHTS_ON, ON, OFF, DIM, BRIGHT,
    ALL_LIGHTS_OFF, EXTENDED_CODE, HAIL_REQUEST, HAIL_ACKNOWLEDGE,
    PRE_SET_DIM, EXTENDED_DATA, STATUS_ON, STATUS_OFF, STATUS_REQUEST };

byte HouseCodeReceived;
byte UnitNumberReceived;
byte CommandReceived;

int incomingByte = 0;
byte packetBuffer[64];
int i = 0;

void setup() {

  Serial.begin(9600);
  Serial.println("Started");

  // Initialize the x10 pins
  // 4 receive data - NOT USED BUT SET TO INPUT
  // 4 transmit data
  // 2 zero crossing
  x10.begin();


}

void loop() {
  int packetSize;
  char *packetType;

  // check for input
  if (Serial.available() > 0) {
    // read the incomming byte:
    packetBuffer[i] = Serial.read();

#ifdef DEBUG
    // echo character recieved
    Serial.write("d2:");
    if ( i < 3 ) Serial.write(packetBuffer[i]);
#endif

    // check if the last character was an EOL
    if (packetBuffer[i] == 10 || packetBuffer[i] == 13) {
      // CR or LF received
      // set the last character to null
      packetBuffer[i] = 0;
      // save the packet size
      packetSize = i;
      // reset the pointer
      i = 0;

#ifdef DEBUG
      // Report packet received
      Serial.write("d3");
#endif

      // We may have a string so lets process it

      //---------------------------------------------------
      // Process Serial data
      // put in check for packetSize
      //---------------------------------------------------

      packetType = "X"; // Default packet expected is 'X'10

      // Check if we have data

#ifdef DEBUG
      Serial.write("d4:");
      Serial.write(packetSize);
#endif
      if (packetSize) {

        // we have a packet available
#ifdef DEBUG
//        Serial.print("Received packet of size ");
//        Serial.println(packetSize);
#endif

#ifdef DEBUG
        Serial.write(" Contents:");
        Serial.write((char*) packetBuffer);
#endif

        // Start with first byte in packet
        i = 0;

        // We have a packet so we need to check it out

        if (packetBuffer[i] > 64 && packetBuffer[i] < 81) {
          // Good house code or T
          HouseCodeReceived = HouseCode[packetBuffer[i] - 65];
          

#ifdef DEBUG
          Serial.write("HC=");
          Serial.print(HouseCodeReceived, BIN);
#endif
          i++;

          switch (packetSize) {
          case 3:
//            Serial.print("d5:");
//            Serial.print(packetBuffer[i]);
            // The next digit is a unit number in hex
            if (validHex(packetBuffer[i])) {
              UnitNumberReceived = UnitNum[hexCharToIndex(
                  packetBuffer[i])];
            } else {
              packetType = "B";
            }

#ifdef DEBUG
            Serial.write("Unit=");
            Serial.print(UnitNumberReceived, BIN);
#endif

            i++;

          case 2:
//            Serial.print("d6:");
//            Serial.print(packetBuffer[i]);
            // The next digit is a command in hex
            if (validHex(packetBuffer[i])) {
              CommandReceived = Cmd[hexCharToIndex(
                  packetBuffer[i])];
            } else {
              packetType = "B";
            }

#ifdef DEBUG
            Serial.write("Cmd=");
            Serial.print(CommandReceived, BIN);
#endif

            break;

          default:
            // Wrong packetSize
//            Serial.write("dBP1");
            packetType = "B";
          }

        } else {
          // Bad packet received
//          Serial.write("dBP2");
          packetType = "B";
        }

        // reset pointer
        i = 0;

#ifdef DEBUG
        if (packetType == "B") {
          Serial.write("badPacket");
        }
#endif
//        Serial.write("d8");
        if (packetType == "X") {
          // We Send the X10 Data
  //        Serial.write("d9");
#ifdef X10SEND
  //        Serial.write("d10");

//#ifdef DEBUG
//Serial.print("::loop():HouseCode=");
//Serial.println(HouseCodeReceived, BIN);
//Serial.print("::loop():Cmd=");
//Serial.println(CommandReceived, BIN);
//#endif
//          Serial.write("x1");
          x10.beginTransmission(HouseCodeReceived);
          //x10.beginTransmission(B);
//          Serial.write("x2");
          if (packetSize == 3) {
//            Serial.write("x3");
            x10.write(UnitNumberReceived);
          }
//          Serial.write("x4");
          x10.write(CommandReceived);
//          Serial.write("x5");
          x10.endTransmission();
//          Serial.write("x6");

#endif

          Serial.println("OK");

        } else {

          Serial.println("ERR");

        }

      } else {
        // We have no data

#ifdef DEBUG
        Serial.println("No Data");
#endif

      }

    } else {

      // more characters expected
      // increment pointer
      i++;
    }
  }

}

//
// convert character to an index (0 based)
//

int hexCharToIndex(byte character) {
  int i;
  i = character - 48;
  if (i > 9) {
    i = i - 7;
  }

  return i;
}

//
// Check if character is a valid HEX digit
// 0-9 and A-F
//

boolean validHex(byte character) {
  if (character > 47 && character < 58) {
    return true;
  } else if (character > 64 && character < 71) {
    return true;
  }
  return false;
}
