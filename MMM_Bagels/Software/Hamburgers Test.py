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
mmm.update();  

# Action 0
raw_input("Press Enter.") 
mmm.rotateShoulders(80,80)
mmm.rotateElbows(0,0)
mmm.update();
  
# Action 1
raw_input("Press Enter.") 
mmm.ser.close()
quit()
