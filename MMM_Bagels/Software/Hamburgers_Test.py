from MMM import MMM
import sys
import time

# Create an MMM
mmm = MMM('/dev/cu.usbmodem1421');

# initial pose
mmm.setWheelVelocity(0,0)
mmm.rotateShoulders(90,90)
mmm.rotateElbows(30,30)
mmm.extendArms(0,0)
mmm.setLeftGrippers(0,87,0,0,0)
mmm.setRightGrippers(0,82,0,0,0)
mmm.update();  

# Action 0: Moving forward
raw_input("Action .5: Press Enter")
mmm.setWheelVelocity(.18, .18)
mmm.update()
time.sleep(1.5)
mmm.setWheelVelocity(0,0)
mmm.update();

# Action 0.5: Setting position
raw_input("Action 0: Press Enter.") 
mmm.rotateShoulders(80,80)
mmm.rotateElbows(-3,3) #Right elbow sinks a little: 6 is offset
mmm.update();



# Action 1: Picking up object
raw_input("Action 1: Press Enter.") 
mmm.rotateShoulders(92,92)
mmm.update();

# Action 1.5: Moving back
raw_input("Action 1.5: Press Enter")
mmm.setWheelVelocity(-.18, -.18)
mmm.update()
time.sleep(1.5)
mmm.setWheelVelocity(0,0)
mmm.update();

# Action 2: Back to original position
#raw_input("Action 2: Press Enter.")
#mmm.rotateElbows(30, 30)
#mmm.rotateShoulders(100, 100)
#mmm.update();

#Action 2.5: Rotate wheels
raw_input("Action 2.5: Press Enter.")
mmm.setWheelVelocity(.18, -.18)
mmm.rotateShoulders(92, 92)
mmm.update()
time.sleep(2.25)
mmm.setWheelVelocity(0, 0)
mmm.rotateShoulders(92, 92)
mmm.update()

# Action 3: Moving forward to box
raw_input("Action .5: Press Enter")
mmm.setWheelVelocity(.18, .18)
mmm.update()
time.sleep(1.5)
mmm.setWheelVelocity(0,0)
mmm.update();

# Action 3.5: Releasing object
raw_input("Action 3: Press Enter.")
mmm.rotateShoulders(80, 80)
mmm.rotateElbows(-5, 1)
mmm.update();


# Action 4: Close program
raw_input("Action 4: Press Enter.")
mmm.ser.close()
quit()
