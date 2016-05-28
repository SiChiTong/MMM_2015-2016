import sys
import time
import json
import serial
import pygame
import XboxController

# Setup Serial Communication to Arduino
ser = serial.Serial('COM4',9600,timeout=1)
ser.readline();


# Initialize variables
leftElbow = 90;
rightElbow = 90;
leftShoulder = 0;
rightShoulder = 0;

def elbowAngleConverter(angle):
  return (angle*120)/180


def sendData(speed1,speed2,leftArm,rightArm,leftShoulder,rightShoulder,leftElbow,rightElbow):
  data =   { 'leftWheel': speed1, 'rightWheel': speed2, 
             #Stepper Motors
             'leftArm':leftArm , 'rightArm':rightArm,
             'leftShoulder':leftShoulder , 'rightShoulder':rightShoulder, 
             #ServoMotors
             'leftElbow':(leftElbow) , 'rightElbow':(rightElbow) }
  dataString = json.dumps(data)  
  dataString = dataString.translate(None, " ")
  
  # send JSON to Arduino
  ser.flush();
  ser.write(dataString)

while True:
  #######Y
  leftElbow = 0#0-180
  rightElbow = 0
  leftShoulder = 0#0-180
  rightShoulder = 0
  speed1 = 0#0-255
  speed2 = 0
  leftArm = 0#0-6400
  rightArm = 0
  sendData(speed1,speed2,leftArm,rightArm,leftShoulder,rightShoulder,leftElbow,rightElbow)
  # Add a short delay
  print("Y")
  time.sleep(4)

  #########M
  leftElbow = 180
  rightElbow = 180
  sendData(speed1,speed2,leftArm,rightArm,leftShoulder,rightShoulder,leftElbow,rightElbow)
  print("M")
  time.sleep(4)

  #########C
  leftElbow = 90
  rightElbow = 180
  sendData(speed1,speed2,leftArm,rightArm,leftShoulder,rightShoulder,leftElbow,rightElbow)
  print("C")
  time.sleep(4)

  #########S
  leftElbow = 180
  rightElbow = 0
  sendData(speed1,speed2,leftArm,rightArm,leftShoulder,rightShoulder,leftElbow,rightElbow)
  print("S")
  time.sleep(4)

  #########The Arm Thing
  rightElbow = leftElbow = 0
  for pump in range(5):
    if pump%2 == 0:
      leftShoulder = rightShoulder = 0
    else:
      leftShoulder = rightShoulder = 180
    sendData(speed1,speed2,leftArm,rightArm,leftShoulder,rightShoulder,leftElbow,rightElbow)
    time.sleep(3) 
    
