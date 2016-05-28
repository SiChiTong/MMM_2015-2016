from MMM import MMM
import sys
import time
import math

# Create an MMM
mmm = MMM('COM3');


def playChord(delay,l1=False,l2=False,l3=False,l4=False,l5=False,
                    r1=False,r2=False,r3=False,r4=False,r5=False):
    # Moves fingers set as True to pressed position
    left1 = 65
    left2 = 60
    left3 = 70
    left4 = 60
    left5 = 65
    right1 = 85
    right2 = 75
    right3 = 75
    right4 = 75
    right5 = 65

    if(l1): left1 = 45
    if(l2): left2 = 40
    if(l3): left3 = 50
    if(l4): left4 = 40
    if(l5): left5 = 45
    if(r1): right1 = 65
    if(r2): right2 = 55
    if(r3): right3 = 55
    if(r4): right4 = 55
    if(r5): right5 = 45

    mmm.setLeftGrippers(l1=left1,l2=left2,l3=left3,l4=left4,l5=left5)
    mmm.setRightGrippers(r1=right1,r2=right2,r3=right3,r4=right4,r5=right5)
    mmm.update()
    time.sleep(delay)

def rotateWrist(leftAngle, rightAngle):
    mmm.setLeftGrippers(l5=leftAngle)
    mmm.setRightGrippers(r5=rightAngle)
    mmm.update()

def updateArms(leftAngle, rightAngle):
    multiplier = 0.75
    mmm.rotateShoulders(multiplier*(90-leftAngle), multiplier*(90-rightAngle))
    rotateWrist(multiplier*(90-leftAngle), multiplier*(90-rightAngle))
    # convert to radians
    leftAngle *= math.pi/180
    rightAngle *= math.pi/180
    # max angle ~40 degrees
    baseLeftLength = 0.41 # meters at 0 degrees
    targetLeftLength = baseLeftLength*(1/math.cos((math.pi/2)-leftAngle))
    leftExtension = targetLeftLength - baseLeftLength
    baseRightLength = 0.41 # meters at 0 degrees
    targetRightLength = baseRightLength*(1/math.cos((math.pi/2)-rightAngle))
    rightExtension = targetRightLength - baseRightLength
    mmm.extendArms(leftExtension, rightExtension)
    print(leftExtension, rightExtension)

    mmm.update()


# taking target key, go to that position
def updateLeftArm(a, b):
    # test vars
    currentLeftKey = a
    targetLeftKey = b

    # stuff
    keyWidth = 7.0/3.0 # in centimeters
    baseLeftLength = 0.41 # meters at 0 degrees

    # current key relative to zero pos of arm
    'currentLeftKey = absLeftKey - startingLeftKey'
    # relative x-pos of arm in meters
    leftPos = (currentLeftKey*(keyWidth))/100
    # amount of keys needed to move by (negative = move left)
    leftKeyChange = targetLeftKey - currentLeftKey
    # distance needed to move in meters (negative = move left)
    leftKeyDist = (leftKeyChange*(keyWidth))/100
    # length between zero pos and target pos
    leftX = leftPos + leftKeyDist
    # target total length of arm
    targetLeftLength = math.sqrt(baseLeftLength**2 +
                                 (abs(leftX))**2)
    # extend arm
    leftExtension = targetLeftLength - baseLeftLength
    mmm.extendLeftArm(leftExtension)
    # resulting target angle
    leftAngle = math.atan((abs(leftX))/baseLeftLength) * 180/math.pi
    # rotate shoulder and wrist based on target angle (and some multiplier?)
    multiplier = 0.75
    mmm.rotateLeftShoulder(multiplier*leftAngle)
    mmm.setLeftGrippers(l5=multiplier*leftAngle)


# taking target key, go to that position
def updateRightArm(a, b):
    # test vars
    currentRightKey = a
    targetRightKey = b

    # stuff
    keyWidth = 7.0/3.0 # in centimeters
    baseRightLength = 0.41 # meters at 0 degrees

    # current key relative to zero pos of arm
    'currentRightKey = absRightKey - startingRightKey'
    # relative x-pos of arm in meters
    rightPos = (currentRightKey*(keyWidth))/100
    # amount of keys needed to move by (negative = move right)
    rightKeyChange = targetRightKey - currentRightKey
    # distance needed to move in meters (negative = move right)
    rightKeyDist = (rightKeyChange*(keyWidth))/100
    # length between zero pos and target pos
    rightX = rightPos + rightKeyDist
    # target total length of arm
    targetRightLength = math.sqrt(baseRightLength**2 +
                                 (abs(rightX))**2)
    # extend arm
    rightExtension = targetRightLength - baseRightLength
    mmm.extendRightArm(rightExtension)
    # resulting target angle
    rightAngle = math.atan((abs(rightX))/baseRightLength) * 180/math.pi
    # rotate shoulder and wrist based on target angle (and some multiplier?)
    multiplier = 0.75
    mmm.rotateRightShoulder(multiplier*rightAngle)
    mmm.setRightGrippers(r5=multiplier*rightAngle)


    
# previous test code
'''
updateArms(0,0)
time.sleep(20)
updateArms(45,45)
time.sleep(10)
updateArms(0,0)
time.sleep(10)

updateArms(15,15)
time.sleep(15)
updateArms(30,30)
time.sleep(15)
updateArms(45,45)
'''
# mmm.rotateShoulders(0.75*(90), 0.75*(90))
# mmm.rotateLeftShoulder(90)
time.sleep(2)
updateLeftArm(0,0)
updateRightArm(0,0)
time.sleep(10)
updateLeftArm(0,5)
updateRightArm(0,5)
time.sleep(10)
updateLeftArm(5,-2)
updateRightArm(5,-2)
time.sleep(10)
updateLeftArm(-2,7)
updateRightArm(-2,7)
time.sleep(10)
updateLeftArm(7,0)
updateRightArm(7,0)

# current error: not doing anything after initializing values...

# Action 2
raw_input("Press Enter.")
mmm.ser.close()
quit()