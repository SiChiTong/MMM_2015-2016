from MMM import MMM
from PIL import Image
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
        print("Going " + str(xCord-self.xPos) + "m in X")
        print("Going " + str(yCord-self.yPos) + "m in Y")
        print("Going to move for " + str(abs(xCord-self.xPos)/0.18) + " seconds")
        time.sleep(abs(xCord-self.xPos)/0.18)
        mmm.setWheelVelocity(0, 0)
        mmm.update()
        self.xPos = xCord
        self.yPos = yCord
        print("Move finished")

    @staticmethod
    def readImage(path):
        img = Image.open(path)
        cols, rows = img.size
        pixelArray = [[0]*cols for x in range(rows)]
        pixels = img.load()
        for row in range(rows):
            for col in range(cols):
                if (pixels[row,col] == (255,255,255)):
                    pixelArray[row][col] = 0
                else:
                    pixelArray[row][col] = 1
        return pixelArray

#Takes a mxm array and convert to robot position
#Return an array of coordinates 
    def arrayToPos(self, pixelArray):
        height = len(pixelArray)
        width = len(pixelArray[0])
        coordArray = []
        for r in range(height):
            for c in range(width):
                if pixelArray[r][c] == 1:
                   coordArray += [(r/100.0,c/100.0)]
        return coordArray

#Takes a coordinate array and let the robot draw according to those coordinates
    def draw(self, coordArray):
         mmm = self.mmm
         counter = 0
         while(counter < len(coordArray)):
             xCord = coordArray[counter][0]
             yCord = coordArray[counter][1]
             self.goTo(xCord, yCord)
             mmm.update()
             time.sleep(10)
             mmm.rotateElbows(-10, 0)
             mmm.update()
             time.sleep(1)
             mmm.rotateElbows(0, 0)
             mmm.update()
             counter = counter + 1        

        
robo = DrawingControl()
robo.mmm.reset()
raw_input("press enter")
pixelArray = [[0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [0,0],
              [1,0]]
pos = robo.arrayToPos(pixelArray)
robo.draw(pos)




    
        
