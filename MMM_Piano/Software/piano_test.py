from MMM import MMM
import sys
import time

# Create an MMM
mmm = MMM('COM3');

# initial pose
mmm.setWheelVelocity(0,0)
mmm.rotateShoulders(120,120)
mmm.rotateElbows(-60,-60)
mmm.extendArms(0,0)
mmm.setLeftGrippers(30,65,60,70,60,65)

mmm.update();  

# Key press position for each finger
raw_input("Press Enter.") 
mmm.setLeftGrippers(30,65,60,70,60,65)
mmm.update()
time.sleep(5)
mmm.setLeftGrippers(30,45,60,70,60,65)
mmm.update()
time.sleep(0.5)
mmm.setLeftGrippers(30,65,40,70,60,65)
mmm.update()
time.sleep(0.5)
mmm.setLeftGrippers(30,65,60,50,60,65)
mmm.update()
time.sleep(0.5)
mmm.setLeftGrippers(30,65,60,70,30,65)
mmm.update()
time.sleep(0.5)
mmm.setLeftGrippers(30,65,60,70,60,45)
mmm.update()
time.sleep(0.5)
  
# Action 2
raw_input("Press Enter.") 
mmm.ser.close()
quit()