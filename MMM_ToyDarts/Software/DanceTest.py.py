import sys
import time
import json
import serial
import pygame
#import XboxController

# Setup Serial Communication to Arduino
ser = serial.Serial('COM3',9600,timeout=1)
ser.readline();

### Setup Xbox controller
##xboxCont = XboxController.XboxController(
##    controllerCallBack = None,
##    joystickNo = 0,
##    deadzone = 0.1,
##    scale = 1,
##    invertYAxis = False)
##xboxCont.start()

# Initialize variables
leftElbow = 90;
rightElbow = 90;
leftShoulder = 0;
rightShoulder = 0;

def move(wheelSpeed1, wheelSpeed2, angle1, angle2, leftShoulder, rightShoulder, leftElbow, rightElbow, delay):
  # Quit when pressing back button
##  if(xboxCont.BACK):
##    xboxCont.stop()
##    ser.close()
##    quit()
##  
##  # Control Wheels with DPAD
##  (horizontal,vertical) = xboxCont.DPAD
##  speed1 = (-horizontal + vertical) * 100
##  speed2 = (horizontal + vertical) * 100
##  
##  # Control Elbows with Joysticks;
##  leftElbow = xboxCont.LTHUMBY*90+90
##  rightElbow = xboxCont.RTHUMBY*90+90
##  #leftElbow += xboxCont.LTHUMBY*3
##  #rightElbow += xboxCont.RTHUMBY*3
##  
##  leftElbow = max(min(leftElbow, 180), 0)
##  rightElbow = max(min(rightElbow, 180), 0)
##  
##  # Control Elbows with Joysticks;
##  leftShoulder += xboxCont.LTHUMBX*5
##  rightShoulder += xboxCont.RTHUMBX*5
##  
##  leftShoulder = max(min(leftShoulder, 180), 0)
##  rightShoulder = max(min(rightShoulder, 180), 0)
  
  # Prepare JSON
             #Motor Controller
  data =   { 'leftWheel': wheelSpeed1, 'rightWheel': wheelSpeed2, 
             #Stepper Motors
             'leftArm':angle1 , 'rightArm':angle2,
             'leftShoulder':leftShoulder , 'rightShoulder':rightShoulder, 
             #ServoMotors
             'leftElbow':leftElbow , 'rightElbow':rightElbow }
  dataString = json.dumps(data)  
  dataString = dataString.translate(None, " ")
  
  # send JSON to Arduino
  ser.flush();
  ser.write(dataString)
  print dataString+"\n"
  
  # Add a short delay
  time.sleep(delay)

# Main Loop
while(True):
  move(50, -50, 0, 0, 0, 0, 0, 180, 2)
  move(50, -50, 0, 0, 0, 0, 180, 0, 2)
  move(50, -50, 0, 0, 0, 0, 180, 180, 5)
  move(-50, 50, 0, 0, 0, 0, 0, 180, 2)
  move(-50, 50, 0, 0, 0, 0, 180, 0, 2)
  move(-50, 50, 0, 0, 0, 0, 0, 0, 5)
  
 
