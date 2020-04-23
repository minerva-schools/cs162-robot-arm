#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// LIMIT FROM 0 TO 180 DEGREES
#define SERVOMIN1  50 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX1  478 // This is the 'maximum' pulse length count (out of 4096)

// LIMIT FROM 0 TO 90 DEGREES
#define SERVOMIN2  239 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX2  478 // This is the 'maximum' pulse length count (out of 4096)

// LIMIT FROM 0 TO 90 DEGREES
#define SERVOMIN3  220 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX3  478 // This is the 'maximum' pulse length count (out of 4096)

#define SERVOMIN4  50 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX4  478 // This is the 'maximum' pulse length count (out of 4096)

#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

int incomingByte;      // a variable to read incoming serial data into

// servo # counter
uint8_t servonum = 0;

void setup() {
  Serial.begin(9600);
  pwm.begin();
  // In theory the internal oscillator is 25MHz but it really isn't
  // that precise. You can 'calibrate' by tweaking this number till
  // you get the frequency you're expecting!
  pwm.setOscillatorFrequency(27000000);  // The int.osc. is closer to 27MHz  
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  delay(10);

}

int angleToPulses1(int ang){
   int pulse = map(ang,0, 180, SERVOMIN1,SERVOMAX1);// map angle of 0 to 180 to Servo min and Servo max 
   return pulse;
}

int angleToPulses2(int ang){
   int pulse = map(ang,0, 90, SERVOMIN2,SERVOMAX2);// map angle of 0 to 180 to Servo min and Servo max 
   return pulse;
}

int angleToPulses3(int ang){
   int pulse = map(ang,0, 90, SERVOMIN3,SERVOMAX3);// map angle of 0 to 180 to Servo min and Servo max 
   return pulse;
}

int angleToPulses4(int ang){
   int pulse = map(ang,0, 180, SERVOMIN4,SERVOMAX4);// map angle of 0 to 180 to Servo min and Servo max 
   return pulse;
}

void home() {
  
  pwm.setPWM(1, 0, angleToPulses2(90));
  delay(500);
  pwm.setPWM(2, 0, angleToPulses3(0));
  delay(500);
  pwm.setPWM(1, 0, angleToPulses2(0));
  delay(500);
  for (int i = 90; i >= 0; i--) {
  pwm.setPWM(0, 0, angleToPulses1(i));    
  delay(20);
  }

}

void location1() {
  
  pwm.setPWM(1, 0, angleToPulses2(90));
  delay(500);
  pwm.setPWM(2, 0, angleToPulses3(39));
  delay(500);
  pwm.setPWM(1, 0, angleToPulses2(75));
  delay(500);
  pwm.setPWM(0, 0, angleToPulses1(35));    
  delay(500);
}

void location2() {
  
  pwm.setPWM(1, 0, angleToPulses2(90));
  delay(500);
  pwm.setPWM(2, 0, angleToPulses3(0));
  delay(500);
  pwm.setPWM(1, 0, angleToPulses2(90));
  delay(500);
  pwm.setPWM(0, 0, angleToPulses1(90));    
  delay(500);
}

void loop (){

// see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    // if it's a capital H (ASCII 72), Go to the origin:
    if (incomingByte == 'H') {
      home();    }
    // if it's an L go to the preset location 1 used for testing the accuracy:
    if (incomingByte == 'L') {
      location1();    
      }

   if (incomingByte == 'M') {
      location2();    
      }
  }
}
