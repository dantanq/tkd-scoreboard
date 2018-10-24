// TaeKwonDo Scoring App
// Author: Danica Tanquilut
// Last Updated: October 2018
// 

// define pin numbers
const int redScorePin1 = 2;
const int redScorePin2 = 4;
const int redScorePin3 = 6;
const int blueScorePin1 = 3;
const int blueScorePin2 = 5;
const int blueScorePin3 = 7;

// define debounce and button delays
const int debounceDelay = 50; //  50 ms
const int buttonDelay = 1000; //  1000 ms = 1 seconds

typedef struct Fighter {
  // input pins
  int scorePin1;
  int scorePin2;
  int scorePin3;
  // previous readings from input pins
  int scoreButton1LastState;
  int scoreButton2LastState;
  int scoreButton3LastState;
  // current readings from input pins
  int scoreButton1State;
  int scoreButton2State;
  int scoreButton3State;
  // serial output when point is detected
  int serialOutput;
  // use for debouncing inputs
  unsigned long lastDebounceTime1;
  unsigned long lastDebounceTime2;
  unsigned long lastDebounceTime3;
  unsigned long lastPress1;
  unsigned long lastPress2;
  unsigned long lastPress3;
  bool push1;
  bool push2;
  bool push3;
} Fighter;

// initialize fighters
struct Fighter* red = (Fighter*) malloc(sizeof(struct Fighter));
struct Fighter* blue = (Fighter*) malloc(sizeof(struct Fighter));

void setup() {
  Serial.begin(9600);

  // initialize pins
  pinMode(redScorePin1, INPUT_PULLUP);
  pinMode(redScorePin2, INPUT_PULLUP);
  pinMode(redScorePin3, INPUT_PULLUP);
  pinMode(blueScorePin1, INPUT_PULLUP);
  pinMode(blueScorePin2, INPUT_PULLUP);
  pinMode(blueScorePin3, INPUT_PULLUP);

  // initialize fighter pin and button states
  // red fighter
  red->scorePin1 = redScorePin1;
  red->scorePin2 = redScorePin2;
  red->scorePin3 = redScorePin3;
  red->scoreButton1LastState = HIGH;
  red->scoreButton2LastState = HIGH;
  red->scoreButton3LastState = HIGH;
  red->lastDebounceTime1 = 0;
  red->lastDebounceTime2 = 0;
  red->lastDebounceTime3 = 0;
  red->serialOutput = 0;
  red->push1 = false;
  red->push2 = false;
  red->push3 = false;
  // blue fighter
  blue->scorePin1 = blueScorePin1;
  blue->scorePin2 = blueScorePin2;
  blue->scorePin3 = blueScorePin3;
  blue->scoreButton1LastState = HIGH;
  blue->scoreButton2LastState = HIGH;
  blue->scoreButton3LastState = HIGH;
  blue->lastDebounceTime1 = 0;
  blue->lastDebounceTime2 = 0;
  blue->lastDebounceTime3 = 0;
  blue->serialOutput = 1;
  blue->push1 = false;
  blue->push2 = false;
  blue->push3 = false;
}

void updateScore(Fighter *fighter) {
  // read input pin's states
  int scoreState1 = digitalRead(fighter->scorePin1);
  int scoreState2 = digitalRead(fighter->scorePin2);
  int scoreState3 = digitalRead(fighter->scorePin3);
  
  // update debounce times
  if (fighter->scoreButton1LastState != scoreState1) {
    fighter->lastDebounceTime1 = millis();
  } 
  
  if (fighter->scoreButton2LastState != scoreState2) {
    fighter->lastDebounceTime2 = millis();
  } 
  
  if (fighter->scoreButton3LastState != scoreState3) {
    fighter->lastDebounceTime3 = millis();
  } 
  
  // now is current time
  unsigned long now = millis();

  // check debounce delays for each button
  if ((now - fighter->lastDebounceTime1) > debounceDelay) {
    // check if button state has changed
    if (scoreState1 != fighter->scoreButton1State) {
      fighter->scoreButton1State = scoreState1;
    }
    if (fighter->scoreButton1State == 0) {
      fighter->lastPress1 = fighter->lastDebounceTime1;
      fighter->push1 = true;
    }
  }
  
  if ((now - fighter->lastDebounceTime2) > debounceDelay) {
    // check if button state has changed
    if (scoreState2 != fighter->scoreButton2State) {
      fighter->scoreButton2State = scoreState2;
    }
    if (fighter->scoreButton2State == 0) {
      fighter->lastPress2 = fighter->lastDebounceTime2;
      fighter->push2 = true;
    }
  }
  
  if ((now - fighter->lastDebounceTime3) > debounceDelay) {
    // check if button state has changed
    if (scoreState3 != fighter->scoreButton3State) {
      fighter->scoreButton3State = scoreState3;
    }
    if (fighter->scoreButton3State == 0) {
      fighter->lastPress3 = fighter->lastDebounceTime3;
      fighter->push3 = true;
    }
  }

  // logical combinations of inputs and whether debounce times are within 1 second
  bool oneTwo = (abs(fighter->lastPress1 - fighter->lastPress2) < buttonDelay) & fighter->push1 & fighter->push2;
  bool oneThree = (abs(fighter->lastPress1 - fighter->lastPress3) < buttonDelay) & fighter->push1 & fighter->push3;
  bool twoThree = (abs(fighter->lastPress3 - fighter->lastPress2) < buttonDelay) & fighter->push2 & fighter->push3;
  // if any are true, Serial print output of fighter (0 for red, 1 for blue)
  if ((oneTwo || oneThree || twoThree)) {
    Serial.println(fighter->serialOutput);
    fighter->push1 = false;
    fighter->push2 = false;
    fighter->push3 = false;
  }

  // save loop's readings as last state
  fighter->scoreButton1LastState = scoreState1;
  fighter->scoreButton2LastState = scoreState2;
  fighter->scoreButton3LastState = scoreState3;
}

void loop() {
  updateScore(red);
  updateScore(blue);
}
