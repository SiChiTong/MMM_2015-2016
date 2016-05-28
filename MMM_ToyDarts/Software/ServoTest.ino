#include <Servo.h>

Servo servo1; //lower servo
Servo servo2;//upper servo
int pos1 = 0;
int pos2 = 0;

void setup() {
  servo1.attach(9);
  servo2.attach(10);
  for(pos1 = 180; pos1 >= 0; pos1 -= 1) // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    servo2.write(pos1);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  } 
  delay(100);
  for(pos2 = 0; pos2 <= 180; pos2 += 1) // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    servo1.write(pos2);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  } 
  
  
}

void loop() {
  
}
