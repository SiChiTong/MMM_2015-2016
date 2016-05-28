# By "Matt" Yixiu Zhao
from MMM import MMM
import sys
import math
import time


SHOULDER_WIDTH = 0.293
SHOULDER_ELBOW = 0.089
ARM_LENGTH_MIN = 0.258
ARM_LENGTH_MAX = ARM_LENGTH_MIN + 0.127

# Positive directions
# wrist Down
# rotate Clockwise
# release Up

# Unit: meters
def distance(dx, dy, dz = 0):
    return (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5

# This function assumes default wrist servo is the first one

# It resets all other grippers so run it before doing anything else!
#                                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Positive direction: x: right, y:front, z: up
def handToPosition(robot, x, y, z, hand = None):

    # if hand not in ["left", "right"]: 
    #     raise Exception "Invalid hand specification!"

    origin_y = 0
    origin_x = -SHOULDER_WIDTH if hand == "left" else SHOULDER_WIDTH

    x = x - origin_x
    y = y - origin_y

    # calculate how long arm needs to extend
    # distance is shorter because of the length of the elbow
    planar_distance = distance(x, y) - SHOULDER_ELBOW
    arm = distance(planar_distance, z)

    if arm > ARM_LENGTH_MAX: 
        # arm exceeds maximum length
        return False

    arm -= ARM_LENGTH_MIN

    angle_horizontal = math.degrees(math.atan2(y, x))
    angle_vertical = math.degrees(math.asin(z / arm))

    grippers = -angle_vertical
    if hand == "left": 
        arms = (arm, 0)
        shoulders = (180 - angle_horizontal, 0) # symmetry
        elbows = (angle_vertical, 0)
        #robot.setLeftGrippers(r1 = grippers)
    elif hand == "right":
        arms = (0, arm)
        shoulders = (0, angle_horizontal)
        elbows = (0, angle_vertical)
        #robot.setRightGrippers(r1 = grippers)

    print ("Arms: ", arms)
    print ("Shoulders: ", shoulders)
    print("Elbows: ", elbows)
    print("Grippers: ", grippers)
    robot.rotateShoulders(shoulders[0], shoulders[1])
    robot.rotateElbows(elbows[0], elbows[1])
    robot.extendArms(arms[0], arms[1])

#         left hand , right hand
# return (x1, y1, z1, x2, y2, z2)
def getHandPosition(robot):
    # Translate everything back to real-life coordinates
    l_shoulder = robot.translate(robot.leftShoulder, 0, 180, 0, 120)
    l_arm = robot.translate(robot.leftArm, ARM_LENGTH_MIN,
        ARM_LENGTH_MAX, 0, 0.127)
    l_elbow = robot.translate(robot.leftElbow, 0, 180, -60, 60)
    r_shoulder = robot.translate(robot.rightShoulder, 0, 180, 0, 120)
    r_arm = robot.translate(robot.rightArm, ARM_LENGTH_MIN,
        ARM_LENGTH_MAX, 0, 0.127)
    r_elbow = robot.translate(robot.rightElbow, 0, 180, -60, 60)

    l_arm_proj = l_arm * math.cos(l_elbow)
    z1 = l_arm * math.sin(l_elbow)
    x1 = - SHOULDER_WIDTH - l_arm_proj * math.cos(l_shoulder)
    y1 = l_arm_proj * math.sin(l_shoulder)

    r_arm_proj = r_arm * math.cos(r_elbow)
    z2 = r_arm * math.sin(r_elbow)
    x2 = SHOULDER_WIDTH + r_arm_proj * math.cos(r_shoulder)
    y2 = r_arm_proj * math.sin(r_shoulder)

    return (x1, y1, z1, x2, y2, z2) 

mmm = MMM('/dev/cu.usbmodem1411'); 
# initial pose
mmm.setWheelVelocity(0,0)
#mmm.rotateShoulders(100,100) #initialize to straight forward (0 is far out, 120 forward)
mmm.rotateShoulders(0,0) #initialize to facing out
                         #to avoid table when raising (0 is far out, 120 forward)
mmm.rotateElbows(60, 60) #initialize to down
mmm.extendArms(0,0)
mmm.setLeftGrippers(0,0,0,0,0)
mmm.setRightGrippers(0,0,0,0,0) #using right grippers 1-3
#r1 wristUpDown   r2 wristRotation    r3 release
mmm.update()

raw_input("Press Enter.") 
print "Raise arms & adjust wrist"
#handToPosition(mmm, SHOULDER_WIDTH, 0.4, 0, "right")
mmm.update()


