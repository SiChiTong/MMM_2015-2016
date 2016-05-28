# By Brendan
# Edited by Matt on 02/13

from MMM import MMM
import sys
import time

wristUDi = 110
wristRoti = 90
releasei = 180

wristUDo = 20

# Create an MMM
mmm = MMM('/dev/cu.usbmodem1411');

# initial pose
mmm.setWheelVelocity(0,0)
#mmm.rotateShoulders(100,100) #initialize to straight forward (0 is far out, 120 forward)
mmm.rotateShoulders(0,0) #initialize to facing out
                         #to avoid table when raising (0 is far out, 120 forward)
mmm.rotateElbows(60, 60) #initialize to down
mmm.extendArms(0,0)
mmm.setLeftGrippers(0,0,0,0,0)
mmm.setRightGrippers(wristUDi,wristRoti,releasei,0,0) #using right grippers 1-3
#r1 wristUpDown   r2 wristRotation    r3 release
mmm.update()

raw_input("Press Enter.") 
print "Raise arms & adjust wrist"
time.sleep(4) #wait for intialize to finish
mmm.rotateElbows(-60, 15) #raise right elbow to be level
mmm.setRightGrippers(wristUDi-wristUDo,wristRoti,releasei,0,0) #adjust wristUD to slightly rotated up
mmm.update()

print "Move right arm to be above table and lego"
time.sleep(4)
mmm.rotateShoulders(0, 100)
mmm.update()

print "Lower right arm a little to grab lego"
time.sleep(4)
mmm.rotateElbows(-60, -5)
mmm.update()

time.sleep(2)
mmm.setRightGrippers(wristUDi,wristRoti,releasei,0,0) #adjust wristUD to slightly rotated down
mmm.update()

print "Raise arm with lego"
time.sleep(4)
mmm.rotateElbows(-60, 15) #raise arm
mmm.setRightGrippers(wristUDi,wristRoti,releasei,0,0) #adjust wristUD to be flat
mmm.update()

print "have fun, by moving arm right"
time.sleep(4)
mmm.rotateShoulders(0, 80)
mmm.update()

# print "have fun, put block down"
# time.sleep(4)
# mmm.rotateElbows(-60, 0) #lower arm all way
# mmm.setRightGrippers(wristUDi-wristUDo,wristRoti,releasei - 30,0,0) #adjust wristUD to slightly up
# mmm.update()

print "have fun, release block while raising arm"
time.sleep(2)
mmm.setRightGrippers(wristUDi,wristRoti,releasei - 30,0,0) #adjust wrist to be flat while release
mmm.rotateElbows(-60, 15) #raise arm while releasing
mmm.update()

time.sleep(5)

print "Finish"
mmm.ser.close()
quit()
