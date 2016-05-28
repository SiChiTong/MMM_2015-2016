from MMM import MMM
import sys
import time

# Create an MMM
mmm = MMM('COM3');

# initial pose
mmm.setWheelVelocity(0,0)
mmm.rotateShoulders(100,100)
mmm.rotateElbows(-60,-60)
mmm.extendArms(0,0)
mmm.setLeftGrippers(0,0,0,0,0,0,0)
mmm.setRightGrippers(0,0,0,0,0,0,0)
mmm.update();  

# Action 0
raw_input("Press Enter.") 
mmm.setWheelVelocity(.18,-.18)
mmm.update()
time.sleep(5)
mmm.setWheelVelocity(0,0)
mmm.update()      

# Action 1
raw_input("Press Enter.") 
mmm.rotateElbows(60,-60)
mmm.extendArms(.027,0)
mmm.update()
  
# Action 2
raw_input("Press Enter.") 
mmm.ser.close()
quit()