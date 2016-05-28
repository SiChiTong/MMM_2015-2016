from MMM import MMM
import sys
import time

class DrawingControl:
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
        self.mmm = MMM('/dev/cu.usbmodem1411')
        self.mmm.rotateElbows(0, -60)
        self.mmm.update()

    def goTo(self, xCord, yCord):
        # arms for y coordinates, wheels for x coordinates
        mmm = self.mmm
        mmm.extendArms(yCord, 0)
        if (xCord-self.xPos < 0):
            mmm.setWheelVelocity(-.18, -.18)
        elif (xCord-self.xPos > 0):
            mmm.setWheelVelocity(0.18, 0.18)
        mmm.update()
        time.sleep(abs(xCord-self.xPos)/0.18)
        mmm.setWheelVelocity(0, 0)
        mmm.update()
        self.xPos = xCord
        self.yPos = yCord

#Takes a mxm array and convert to robot position
#Return an array of coordinates 
    def arrayToPos(self, pixelArray):
        length = len(pixelArray)
        coordArray = [None] * (length * length)
        counter = 0
        for r in range(length):
            for c in range(length):
                if pixelArray[r][c] == 1:
                   coordArray[counter] = (r,c)
        return coordArray

#Takes a coordinate array and let the robot draw according to those coordinates
    def draw(self, coordArray):
         mmm = self.mmm
         counter = 0
         while(counter < len(coordArray) and coordArray[counter] != None):
             xCord = coordArray[counter][0]
             yCord = coordArray[counter][1]
             self.goTo(xCord, yCord)
             counter = counter + 1
        

        
robo = DrawingControl()
raw_input("Press Enter.")
robo.draw([(0,0.02)])



    
        
