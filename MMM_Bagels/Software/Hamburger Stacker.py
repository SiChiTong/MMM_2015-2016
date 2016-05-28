from MMM import MMM
import sys
import time
import math

#Distances:
#Shoulder to ground: .786 meters
#Shoulder length: .248 meters
#Length of shoulder-hand connection: .007 meters
#Total length from elbow to hand when outstretched: .337 meters
#Length from elbow alone: .082 meters

def calculateShoulderAngle(tableHeight):
    #Todo: calculate shoulder length with hand attached and set to pickup pos
    armLength = .248 #In meters
    shoulderHeight = .786
    targetHeight = tableHeight + .01
    deltaHeight = shoulderHeight - targetHeight
    shoulderAngle = math.acos(deltaHeight/armLength) 
    #In radians, convert to degrees
    return (shoulderAngle * 2*math.pi)//360

# Create an MMM
mmm = MMM('/dev/cu.usbmodem1421');

# initial pose

def restingPosition():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(90,90)
    mmm.rotateElbows(30,30)
    mmm.extendArms(0,0)
    mmm.setLeftGrippers(0,87,0,0,0)
    mmm.setRightGrippers(0,82,0,0,0)
    mmm.update();  

velocity = .18 #meters per second, max speed of wheels
REoffset = 6 #Right elbow sinks a little, this is to offset this fact
d = .27 #Distance in meters to table

def moveForward(distance):
    movingTime = distance / velocity
    mmm.setWheelVelocity(velocity, velocity)
    mmm.update()
    time.sleep(movingTime)
    mmm.setWheelVelocity(0,0)
    mmm.update();

def moveBackwards(distance):
    movingTime = distance / velocity
    mmm.setWheelVelocity(-velocity, -velocity)
    mmm.update()
    time.sleep(movingTime)
    mmm.setWheelVelocity(0,0)
    mmm.update();

def rotateBody(angle): #Negative is counterclockwise, positive is clockwise
    if angle == 0 or abs(angle) > 360: return
    elif angle < 0:
        mmm.setWheelVelocity(.18, -.18)
    elif angle > 0:
        mmm.setWheelVelocity(-.18, .18)
    rotationTime = abs(angle) / 40 #Turns 40 degrees/second
    mmm.rotateShoulders(92, 92)
    mmm.update();
    time.sleep(rotationTime)
    mmm.setWheelVelocity(0, 0)
    mmm.rotateShoulders(92, 92)
    mmm.update();

def releaseObject():
    mmm.rotateShoulders(80, 80)
    mmm.rotateElbows(-5, 1)
    mmm.update();

def readyPosition():
    mmm.rotateShoulders(80,80)
    mmm.rotateElbows(-3,-3 + REoffset)
    mmm.update();

# Action 0: resting position
restingPosition();

# Assume items are .1 meters apart, lined up sequentially
def stackHamburger(numObjects, objectOffset = .1):
    if numObjects < 0: return "Error: invalid number of objects to move."
    elif numObjects == 0: return "Done" #Base case
    # Action 1: Turn to move to object
    raw_input("Action 1: Press Enter")
    rotateBody(90);

    # Action 2: Move in front of object
    raw_input("Action 2: Press Enter")
    moveForward(objectOffset);

    # Action 3: Turn to face object
    raw_input("Action 3: Press Enter")
    rotateBody(-90);

    # Action 4: Moving forward
    raw_input("Action 4: Press Enter")
    moveForward(d);

    # Action 5: Setting position
    raw_input("Action 5: Press Enter.") 
    readyPosition();

    # Action 6: Picking up ingredient
    raw_input("Action 6: Press Enter.") 
    mmm.rotateShoulders(92,92)
    mmm.update();

    # Action 7: Moving back
    raw_input("Action 7: Press Enter")
    moveBackwards(d);

    # Action 8: Rotate wheels 90 degrees CCW
    raw_input("Action 8: Press Enter.")
    rotateBody(-90);

    # Action 9: Move in front of assembly area
    raw_input("Action 9: Press Enter")
    moveForward(objectOffset);

    # Action 10: Turn towards assembly area
    raw_input("Action 10: Press Enter")
    rotateBody(90);

    # Action 11: Move towards assembly area
    raw_input("Action 11: Press Enter")
    moveForward(d);

    # Action 12: Releasing object
    raw_input("Action 12: Press Enter.")
    releaseObject();

    # Action 13: Move back
    raw_input("Action 13: Press Enter")
    moveBackwards(d);

    stackHamburger(numObjects - 1, objectOffset + .1);

# Stack x number of objects onto the bun
stackHamburger(1);

# Action n: Close program
raw_input("Action n: Press Enter to quit.")
mmm.ser.close()
quit();
