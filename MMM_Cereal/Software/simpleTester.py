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

'''
wheel(x,x)
shoulder(x,x)
elbow(x,x)
arm(x,x)
left(x,x)
right(x,x)
'''

while True:
    s = input('-->')
    if(s.startswith('wheel')):
        command = s[len('wheel'):]
        command = eval(command)
        mmm.setWheelVelocity(*command)
    elif(s.startswith('shoulder')):
        command = s[len('shoulder'):]
        command = eval(command)
        mmm.rotateShoulders(*command)
    elif(s.startswith('elbow')):
        command = s[len('elbow'):]
        command = eval(command)
        mmm.rotateElbows(*command)
    elif(s.startswith('arm')):
        command = s[len('arm'):]
        command = eval(command)
        mmm.extendArms(*command)
    elif(s.startswith('left')):
        command = s[len('left'):]
        command = eval(command)
        mmm.setLeftGrippers(*command)
    elif(s.startswith('right')):
        command = s[len('right'):]
        command = eval(command)
        mmm.setRightGrippers(*command)
    elif(s == "quit"):
        break
    mmm.update()

print('bye')

