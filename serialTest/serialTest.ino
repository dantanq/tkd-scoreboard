// Simple app to test if serial output/input is working in TKD Scoring App
// Author: Danica Tanquilut
// Last Updated: October 2018
//

int output;

void setup() {
  Serial.begin(9600);
  output = 0;
}

void loop() {
  Serial.println(output);
  if (output == 0) {
    output = 1;
  } else {
    output = 0;
  }
  delay(2000);
}
