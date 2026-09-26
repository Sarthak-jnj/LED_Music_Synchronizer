byte LED_OT[4] = {3, 5, 9, 11};
void setup() {
for (byte i = 0; i<4; i++) {
  pinMode(LED_OT[i], OUTPUT);
  }
Serial.begin(115200);
}
void loop() {
if (Serial.available() > 1){
  byte Byte_ID = Serial.read() - 'A';
  if (Byte_ID >= 0 && Byte_ID <= 3){
    analogWrite(LED_OT[Byte_ID], Serial.read());
    }
  }
}