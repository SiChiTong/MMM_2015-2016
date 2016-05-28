from MMM import MMM
import sys
import time

# Create an MMM
mmm = MMM('/dev/cu.usbmodem1411');

# initial pose
# mmm.setWheelVelocity(0,0)
# mmm.rotateShoulders(100,100)
# mmm.rotateElbows(-60,-60)
# mmm.extendArms(0,0)
# mmm.setLeftGrippers(0,0,0,0,0)
# mmm.setRightGrippers(0,0,0,0,0)
# mmm.update()

def initialize():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(90,90)
    mmm.rotateElbows(-5,30)
    mmm.extendArms(0,0)
    mmm.setLeftGrippers(135,90,0,0,0)
    mmm.setRightGrippers(30,75,60,0,0)
    mmm.update()

def goToFeedPosition():
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(90,94)
    mmm.rotateElbows(-5,40)
    mmm.extendArms(0,0.127)
    mmm.setLeftGrippers(135,90,0,0,0)
    mmm.setRightGrippers(50,65,50,0,0)
    mmm.update()
goToFeedPosition()
#L2 is the third input

'''
wheel(x,x)
shoulder(x,x)
elbow(x,x)
arm(x,x)
left(x,x)
right(x,x)
L1,60
'''
leftGrippers = [0,0,0,0,0]
rightGrippers = [0,0,0,0,0]

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
        leftGrippers = list(eval(command))
        mmm.setLeftGrippers(*leftGrippers)
    elif(s.startswith('right')):
        command = s[len('right'):]
        rightGrippers = list(eval(command))
        mmm.setRightGrippers(*rightGrippers)
    elif(s.startswith('L')):
        angle = s[len('L')+2:]
        index = eval(s[1]) - 1
        leftGrippers[index] = angle
        mmm.setLeftGrippers(*leftGrippers)
    elif(s.startswith('R')):
        angle = s[len('R')+2:]
        index = eval(s[1]) - 1
        rightGrippers[index] = angle
        mmm.setRightGrippers(*rightGrippers)
    elif(s == "quit"):
        break
    mmm.update()

print('bye')

"""
shoulder 180 180
elbow 0,0
r2 90
r3 unkown
"""
