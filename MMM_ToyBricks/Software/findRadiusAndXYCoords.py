import numpy as np
import cv2
import time
import imutils

# findRadiusAndXYCoords(showFrames=False)
# returns (float radius, float x, float y)
# camera resolution: x = 480, y = 640

def findRadiusAndXYCoords(showFrames = False):
    startTime = time.time()
    radii = list()
    xCoord = list()
    yCoord = list()
    camera = cv2.VideoCapture(0)

    redLower = np.array([0,100,0]) # actually orange
    redUpper = np.array([30,255,255]) # actually orange


    # find the average radius across 5 seconds 
    while ((time.time() - startTime) < 5):
        (grabbed, frame) = camera.read() # grab picture

        print frame.shape
        blurred = cv2.GaussianBlur(frame, (11,11), 0) # apply Gaussian blur
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert to HSV

        mask = cv2.inRange(hsv, redLower, redUpper)
        mask = cv2.dilate(mask, None, iterations=1)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            radii.append(radius)
            
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0,255,255), 2)
                xCoord.append(x)
                yCoord.append(y)
                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.circle(mask, (int(x), int(y)), int(radius),
                    (0,255,255), 2)
                cv2.circle(mask, (int(x), int(y)), 5, (0, 0, 255), -1)

        if showFrames:
            cv2.imshow("Frame", frame)
            cv2.imshow("mask", mask)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    if (len(radii) > 0 and len(xCoord)) > 0:
        radiiSum = 0
        xCoordSum = 0
        yCoordSum = 0

        for i in xrange(len(radii)):
            radiiSum += radii[i]
        averageRadius = radiiSum / len(radii)
        
        for i in xrange(len(xCoord)):
            xCoordSum += xCoord[i]
            yCoordSum += yCoord[i]
        averageX = xCoordSum / len(xCoord)
        averageY = yCoordSum / len(yCoord)

        return averageRadius, averageX, averageY
    else:
        return "no circles detected"

if __name__ == "__main__":
    print(findRadiusAndXYCoords())