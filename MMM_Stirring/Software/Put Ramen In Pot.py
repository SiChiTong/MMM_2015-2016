from MMM import MMM
import sys
import time
import math

# Create an MMM
mmm = MMM('COM3');

def initialPose(mmm):
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(90,90)
    mmm.rotateElbows(0,25)#right arm pointing forward
    mmm.extendArms(0,0)
    mmm.setLeftGrippers(0,0,0,0,0)
    mmm.setRightGrippers(0,0,0,0,0)
    mmm.update()
    time.sleep(2)

def driveForward_GrabRamen_AndPutRamenInPot(mmm):

    #This driving code isn't working, but I'm not sure why:
    (wheelVelocity, driveTime) = (0.1, 2)
        #adjust these once the starting location of the robot is decided on
    mmm.setWheelVelocity(wheelVelocity, wheelVelocity)
    mmm.update()
    time.sleep(driveTime)
    mmm.setWheelVelocity(0, 0)
    mmm.update()
    
    #pick up ramen with left arm/hand, then move to pot:
    grabRamen(mmm) #not written yet; depends on hand design
    mmm.rotateElbows(25, 25) #lift up left arm, which is holding ramen block
    mmm.update()
    mmm.rotateShoulders(120, 90) #rotate left arm over to pot
        #may need to adjust left number to accurately place ramen
        #may also need to add arm extension so left hand can reach the pot
    mmm.update()
    dropRamen(mmm) #not written yet; depends on hand design
    
    #now move left arm out of the way:
    mmm.rotateShoulders(90, 90)
    mmm.update()
    mmm.rotateElbows(0, 25)
    mmm.update()

def grabRamen(mmm): #not written yet; depends on hand design
    print("Grab Ramen")

def dropRamen(mmm): #not written yet; depends on hand design
    print("Drop Ramen")

driveForward_GrabRamen_AndPutRamenInPot(mmm)
