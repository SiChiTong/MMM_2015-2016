from MMM import MMM
import sys
import time
import math

# Create an MMM
mmm = MMM('COM3');
cookingTime = 180 #seconds

def initialPose(mmm):
    mmm.setWheelVelocity(0,0)
    mmm.rotateShoulders(90,90)
    mmm.rotateElbows(0,25)#right arm pointing forward
    mmm.extendArms(0,0.05)#arm initially extended slightly,
                          #so it can move forward and backward
    mmm.setLeftGrippers(0,0,0,0,0)
    mmm.setRightGrippers(0,0,0,0,0)
    mmm.update()
    time.sleep(2)

def stir(mmm): #completes one stir cycle
    #move spoon forward, then move left and right while pulling it backward
    (minExtension, maxExtension) = (0, 0.12)
    armMovement = 0.01 #move 1 cm forward/backward each cycle

    cShoulder = 90 #default location of shoulder
    shoulderRotation = 3 #degrees left/right of center

    (minShoulder, maxShoulder) = (cShoulder - shoulderRotation, cShoulder + shoulderRotation)
    mmm.extendArms(0, maxExtension)
    mmm.update()
    time.sleep(2)
    while True:
        mmm.extendArms(0, mmm.rightArm-armMovement)  #pull arm backward slightly
        mmm.update()
        time.sleep(0.5)
        mmm.rotateShoulders(0, minShoulder) #move spoon left
        mmm.update()
        time.sleep(0.5)
        mmm.rotateShoulders(0, maxShoulder) #move spoon right
        mmm.update()
        time.sleep(0.5)
        if (mmm.rightArm - armMovement <= minExtension):
            break

def stirRamen(mmm, cookingTime):
    startTime = time.time()
    endTime = startTime + cookingTime
    currentTime = startTime
    while (currentTime < endTime):
        currentTime = time.time()
        stir(mmm)


initialPose(mmm)
#stirRamen(mmm, cookingTime)

###########################################################################
# Circular Stir Motion (not tested yet)
###########################################################################

def circularStir(mmm):
    t = 0
    timeInterval = 0.5 #seconds; must be long enough for robot to move
    dTheta = math.pi / 4 #move 45 degrees around stirring circle
                         #during each time interval
    endTheta = dTheta * (cookingTime / timeInterval)
    for theta in range(0, endTheta, dTheta):
        #plan a circular path for the robot hand
            #then move along this path each timeInterval

        #figure out where to move arm along circular stirring path
            #circle is parametrized with x = r*sin(t), y = r*cos(t)
        x = math.cos(theta)
        y = math.sin(theta)
        #convert these positions into an arm extension and shoulder angle:
        (extension, angle) = getExtensionAndAngle(x, y)
        mmm.rotateShoulders(0, angle)
        mmm.extendArms(0, extension)
        mmm.update()
        time.sleep(timeInterval)
    print("Done Stirring!")
            
def getExtensionAndAngle(x, y)
    #set up a coordinate system centered at center of pot:
        #2 variables are (extension, angle)
    (extensionAtOrigin, angleAtOrigin) = (0.06, 90) #(meters, degrees)
    (extensionRange, rotationRange) = (0.06, 3) #(meters, degrees)
    extension = extensionAtOrigin + y * extensionRange
    angle = angleAtOrigin + x * rotationRange
    
    print("x = ", x, "y = ", y)
    print("extension = ", extension, "angle = ", angle, "\n")
    return (extension, angle)

circularStir(mmm)
