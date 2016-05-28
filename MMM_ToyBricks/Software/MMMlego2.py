from MMM import MMM
import sys
import time

wristUDi = 90
wristRoti = 90
releasei = 160

wristUDo = 20

# Create an MMM
mmm = MMM('COM3');

# initial pose
mmm.setWheelVelocity(0,0)
#mmm.rotateShoulders(100,100) #initialize to straight forward (0 is far out, 120 forward)
mmm.rotateShoulders(0,0) #initialize to facing out
                         #to avoid table when raising (0 is far out, 120 forward)
mmm.rotateElbows(-60,-60) #initialize to down
mmm.extendArms(0,0)
mmm.setLeftGrippers(0,0,0,0,0)
mmm.setRightGrippers(wristUDi,wristRoti,releasei,0,0) #using right grippers 1-3
#r1 wristUpDown   r2 wristRotation    r3 release
mmm.update()

#raw_input("Press Enter.") 
#mmm.update()

# Raise arms & adjust wrist
time.sleep(5) #wait for intialize to finish
mmm.rotateElbows(-60, 0) #raise right elbow to be level
mmm.setRightGrippers(wristUDi-wristUDo,wristRoti,releasei,0,0) #adjust wristUD to slightly rotated up
mmm.update()

# Move right arm to be above table and lego
time.sleep(5)
mmm.rotateShoulders(0, 100)
mmm.update()

# Lower right arm a little to grab lego
time.sleep(5)
mmm.rotateElbows(-60, -20)
mmm.update()

# Raise arm with lego
time.sleep(5)
mmm.rotateElbows(-60, 0) #raise arm
mmm.setRightGrippers(wristUDi,wristRoti,releasei,0,0) #adjust wristUD to be flat
mmm.update()

# have fun, by moving arm right
time.sleep(5)
mmm.rotateShoulders(0, 80)
mmm.update()

# have fun, put block down
time.sleep(5)
mmm.rotateElbows(-60, -20) #lower arm all way
mmm.setRightGrippers(wristUDi-wristUDo,wristRoti,releasei,0,0) #adjust wristUD to slightly up
mmm.update

# have fun, release block while raising arm
time.sleep(5)
mmm.setRightGrippers(wristUDi,wristRoti,releasei-30,0,0) #adjust wrist to be flat while release
mmm.rotateElbows(-60, 0) #raise arm while releasing
mmm.update

mmm.sleep(5)

# Finish
mmm.ser.close()
quit()
