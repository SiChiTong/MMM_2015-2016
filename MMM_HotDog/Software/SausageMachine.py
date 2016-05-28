from MMM import MMM
import sys
import time

sausager = MMM('/dev/cu.usbmodem1411');

#move towards table
sausager.rotateShoulders(80,80)
sausager.setWheelVelocity(.18,.18)
sausager.update()
time.sleep(1.66667)
sausager.setWheelVelocity(0,0)
sausager.update() 

raw_input("Press Enter.")
#move arm downwards an grab sausage
sausager.rotateElbows(2,18)
sausager.extendArms(.2,0)
sausager.setLeftGrippers(l2 = 60)
sausager.update()
time.sleep(0.555)
#move arm to original position
sausager.rotateElbows(2,18)
sausager.extendArms(-.2,0)
sausager.update()
time.sleep(.4)

raw_input("Press Enter.")
#move towards bun holder
sausager.setWheelVelocity(.18,.18)
sausager.update()
time.sleep(0.555)
sausager.setWheelVelocity(0,0)
sausager.update() 

raw_input("Press Enter.")
#place sausage in bun
sausager.rotateElbows(-2,18)
sausager.extendArms(.2,0)
time.sleep(0.4)
sausager.setLeftGrippers(l2 = 110)
sausager.update()
sausager.extendArms(-.2,0)
sausager.update()
time.sleep(0.4)

raw_input("Press Enter.")
#move to original position
sausager.setWheelVelocity(-.18,-.18)
sausager.update()
time.sleep(2.222)
sausager.setWheelVelocity(0,0)
sausager.update()

raw_input("Press Enter.")

#change the angle
sausager.setWheelVelocity(.18,-.18)
sausager.update()
time.sleep(0.6)
sausager.setWheelVelocity(0,0)
sausager.update()

raw_input("Press Enter.")
#move towards the 1st bottle
sausager.setWheelVelocity(.18,.18)
sausager.update()
time.sleep(2.1)
sausager.setWheelVelocity(0,0)
sausager.update()

raw_input("Press Enter.")
#grab the first bottle
sausager.extendArms(0,.2)
time.sleep(0.4)
sausager.setRightGrippers(l2 = 60)
sausager.update()
sausager.rotateElbows(-2,30)
sausager.update()
time.sleep(0.4)

raw_input("Press Enter.")
#move bottle towards bun
sausager.setWheelVelocity(-.18,.18)
sausager.update()
time.sleep(0.3)
#start squeezing the sauce
sausager.rotateElbows(-2,20)
sausager.setRightGrippers(l2 = 40)
sausager.setWheelVelocity(-.18,.18)
sausager.update()
time.sleep(0.1)
sausager.setWheelVelocity(.18,.18)
sausager.update()
time.sleep(0.1)
sausager.setWheelVelocity(.18,-.18)
sausager.update()
time.sleep(0.1)
sausager.setWheelVelocity(.18,.18)
sausager.update()
time.sleep(0.1)

raw_input("Press Enter.")
#return bottle to original position
sausager.setWheelVelocity(.18,-.18)
sausager.update()
time.sleep(0.2)
sausager.rotateElbows(-2,18)
sausager.setRightGrippers(l2 = 110)

raw_input("Press Enter.")
#grab the second bottle
sausager.rotateElbows(-2,30)
sausager.setWheelVelocity(.18,-.18)
sausager.update()
time.sleep(0.1)
sausager.rotateElbows(-2,18)
sausager.extendArms(0,.2)
time.sleep(0.4)
sausager.setRightGrippers(l2 = 60)
sausager.update()
sausager.rotateElbows(-2,30)
sausager.update()
time.sleep(0.4)

raw_input("Press Enter.")
#move bottle towards bun
sausager.setWheelVelocity(-.18,.18)
sausager.update()
time.sleep(0.35)

raw_input("Press Enter.")
#start squeezing the sauce
sausager.rotateElbows(-2,20)
sausager.setRightGrippers(l2 = 40)
sausager.setWheelVelocity(-.18,.18)
sausager.update()
time.sleep(0.1)
sausager.setWheelVelocity(.18,.18)
sausager.update()
time.sleep(0.1)
sausager.setWheelVelocity(.18,-.18)
sausager.update()
time.sleep(0.1)
sausager.setWheelVelocity(.18,.18)
sausager.update()
time.sleep(0.1)

raw_input("Press Enter.")
#return bottle to original position
sausager.setWheelVelocity(.18,-.18)
sausager.update()
time.sleep(0.3)
sausager.rotateElbows(-2,18)
sausager.setRightGrippers(l2 = 110)