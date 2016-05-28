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
mmm.setLeftGrippers(0,0,0,0,0)
mmm.setRightGrippers(0,0,0,0,0)
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


def initialize():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(90,90)
    mmm.rotateElbows(-5,30)
    mmm.extendArms(0,0)
    mmm.setLeftGrippers(135,90,0,0,0)
    mmm.setRightGrippers(30,75,60,0,0)
    mmm.update()

def goToScoopPosition():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(90,94)
    mmm.rotateElbows(-5,25)
    mmm.extendArms(0,0.03)
    mmm.setLeftGrippers(135,90,0,0,0)
    mmm.setRightGrippers(30,45,50,0,0)
    mmm.update()

def goToFeedPosition():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(90,94)
    mmm.rotateElbows(-5,40)
    mmm.extendArms(0,0.127)
    mmm.setLeftGrippers(135,90,0,0,0)
    mmm.setRightGrippers(50,65,50,0,0)
    mmm.update()

def feed():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(90,85)
    mmm.rotateElbows(-5,40)
    mmm.extendArms(0,0.127)
    mmm.setLeftGrippers(135,90,0,0,0)
    mmm.setRightGrippers(50,65,50,0,0)
    mmm.update()

delay(10)

for i in xrange(0,2):

    initialize()
    delay(5)
    goToScoopPosition()
    delay(5)
    goToFeedPosition()
    delay(10)
    feed()
    delay(7)
