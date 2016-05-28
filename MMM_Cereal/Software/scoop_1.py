from MMM import MMM
import sys
import time

# Create an MMM
mmm = MMM('/dev/cu.usbmodem1411');

# initial pose
mmm.setWheelVelocity(0,0)
mmm.rotateShoulders(100,100)
mmm.rotateElbows(-60,-60)
mmm.extendArms(0,0)
mmm.setLeftGrippers(0,0,0,0,0,0,0)
mmm.setRightGrippers(0,0,0,0,0,0,0)
mmm.update()

def delay(n):
    time.sleep(n)

def grabCereal():
    """
    step 0: go back to initial position after feeding
    step 1: move horizontally to to the bowl
    step 2: tilt the spoon to entry position
    step 3: poke down
    step 4: tilt back to normal
    step 5: raise spoon to feed
    
    #steps 1-4 is done with goToScoopPosition
    """
    initializeSpoon()
    delay(1000)
    goToScoopPosition()
    delay(1000)
    goToFeedPosition()
    delay(1000)

def initializeSpoon():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(100,100)
    mmm.rotateElbows(-60,-60)
    mmm.extendArms(0,0)
    mmm.setLeftGrippers(0,0,0,0,0,0,0)
    mmm.setRightGrippers(0,0,0,0,0,0,0)
    mmm.update()

def initializeBowl():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(100,100)
    mmm.rotateElbows(-60,-60)
    mmm.extendArms(0,0)
    mmm.setLeftGrippers(0,0,0,0,0,0,0)
    mmm.setRightGrippers(0,0,0,0,0,0,0)
    mmm.update()

def goToScoopPosition():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(100,100)
    mmm.rotateElbows(-60,-60)
    mmm.extendArms(0,0)
    mmm.setLeftGrippers(0,0,0,0,0,0,0)
    mmm.setRightGrippers(0,0,0,0,0,0,0)
    mmm.update()

def goToFeedPosition():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(100,100)
    mmm.rotateElbows(-60,-60)
    mmm.extendArms(0,0)
    mmm.setLeftGrippers(0,0,0,0,0,0,0)
    mmm.setRightGrippers(0,0,0,0,0,0,0)
    mmm.update()