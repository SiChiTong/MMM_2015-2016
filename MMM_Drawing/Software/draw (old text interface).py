from __future__ import print_function, division
import PIL.Image
import math
import cv2
import numpy
import time
import serial
from Tkinter import *
from MMM import MMM

# Global Parameters
inputPath = "C:/Users/Ian/Desktop/dog.jpg" # Make sure to load square images in RGB format
imWidth, imHeight = PIL.Image.open(inputPath).size
drawWidth, drawHeight = (100,100)
r = 50 # mm radius of the servo motion
timeStep = 0.25 # Probably don't go faster than 0.25
timeStepBetweenContours = 10 # Based on experiments for speed and max distance between contours

#------------------------------------------------------------------------------#

# PIL Stuff

def imageToList(inputPath):
	# Converts a PIL image object to a flat numpy array of RGB tuples
	inputImage = PIL.Image.open(inputPath)
	imageList = list(inputImage.getdata())
	return imageList

def listToImage(imageList, inputImage):
	# Converts a flat numpy array of RGB tuples to a PIL image object
	newImage = PIL.Image.new(inputImage.mode, (imWidth, imHeight))
	newImage.putdata(imageList)
	return newImage

#------------------------------------------------------------------------------#

# OpenCV Stuff

#def invertImage(image):
#def flipImage(image):

def openImage(inputPath):
	# Opens an image with OpenCV
	inputImage = cv2.imread(inputPath)
	return inputImage

def applyThreshold(inputImage):
	# Apply a threshold to the image
	imgray = cv2.cvtColor(inputImage,cv2.COLOR_RGB2GRAY)
	ret, threshold = cv2.threshold(imgray,0,255,cv2.THRESH_OTSU)
	return threshold

def getContours(inputThreshold):
	# Finds the contours of a binary image, returns a numpy array of contours
	im2, contours, hierarchy = cv2.findContours(inputThreshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # RETR_LIST or RETR_EXTERNAL
	return contours

def contoursToImageList(contours, inputPath):
	# Overlays the contours on a list, like an image
	imageList = [(255,255,255)] * imWidth * imHeight
	for contour in contours:
		for point in contour:
			x = point[0][0]
			y = point[0][1]
			imageList[x + y * imWidth] = (0,0,0)
	return imageList

def showContours(contours, inputPath):
	newImageList = contoursToImageList(contours, inputPath)
	newImage = listToImage(newImageList, PIL.Image.open(inputPath))
	newImage.show()

def getContourArray(inputPath):
	inputImage = openImage(inputPath)
	threshold = applyThreshold(inputImage)
	contours = getContours(threshold)
	return contours

#------------------------------------------------------------------------------#

# Coordinate System Stuff

def radiansToDegrees(theta):
	return theta * 180 / math.pi

def resizeImage(coordinates):
	# Resizes a larger square image to a 100x100 square image
	x = coordinates[0]
	y = coordinates[1]
	return (x/imWidth*drawWidth, y/imHeight*drawHeight)

def transformCoordinates(coordinates):
	# Shifts a 
	x = coordinates[0]
	y = coordinates[1]
	return (x-drawWidth/2, drawHeight-y)

def convertCoordinateSystem(coordinates):
	x = coordinates[0]
	y = coordinates[1]
	theta = math.acos(x / r)
	h = y - r * (math.sin(theta) - 1)
	return (radiansToDegrees(theta), h)

def convertContourCoordinates(contours):
	convertedContours = []
	for contour in contours:
		convertedPoints = []
		for point in contour:
			x = point[0][0]
			y = point[0][1]
			convertedPoints += [convertCoordinateSystem(transformCoordinates(resizeImage((x,y))))]
		convertedContours += [convertedPoints]
	return convertedContours

def demo():
	coordinate = (0,0)
	print("point:", coordinate)
	print("resized:", resizeImage(coordinate))
	print("transformed", transformCoordinates(resizeImage(coordinate)))
	print("converted:", convertCoordinateSystem(transformCoordinates(resizeImage((coordinate)))))
	print()
	coordinate = (100,100)
	print("point:", coordinate)
	print("resized:", resizeImage(coordinate))
	print("transformed", transformCoordinates(resizeImage(coordinate)))
	print("converted:", convertCoordinateSystem(transformCoordinates(resizeImage((coordinate)))))

#------------------------------------------------------------------------------#

# Animate Coordinate Drawing

def tkKeyPressed(event):
	global timeDelay
	if event.keysym == "Up":
		timeDelay /= 10
	elif event.keysym == "Down" and timeDelay < 0.1:
		timeDelay *= 10

def tkDrawContours(contours, windowWidth=1000, windowHeight=1000):
	root = Tk()
	canvas = Canvas(root, width=windowWidth, height=windowHeight)
	canvas.pack()
	root.bind("<Key>", lambda event: tkKeyPressed(event))
	global timeDelay
	timeDelay = .01
	contourNumber = 1
	radius = int(windowWidth/100)
	for contour in range(len(contours)):
		for point in range(len(contours[contour])):
			x1 = contours[contour][point][0][0]/imWidth*windowWidth
			y1 = contours[contour][point][0][1]/imHeight*windowHeight
			x2 = contours[contour][(point+1)%len(contours[contour])][0][0]/imWidth*windowWidth
			y2 = contours[contour][(point+1)%len(contours[contour])][0][1]/imHeight*windowHeight
			canvas.create_line(x1, y1, x2, y2, fill="black")
			pointer = canvas.create_oval(x2-radius, y2-radius, x2+radius, y2+radius, fill="red", outline="")
			speed = canvas.create_text((5,0), anchor="nw", text="Speed: " + str(1/timeDelay) + " points/second (Press Up or Down to change)")
			root.update()
			canvas.delete(pointer)
			canvas.delete(speed)
			time.sleep(timeDelay)
		contourNumber += 1
	root.mainloop()


#------------------------------------------------------------------------------#

# Drawing Stuff

def findDrawingTime(convertedContours):
	# Returns estimated drawing time in seconds based on a contour array
	time = 0
	for contour in convertedContours:
		time += len(contour) * timeStep + timeStepBetweenContours + 1
	return time

def draw(inputPath):
	print("Initializing...")
	contours = getContourArray(inputPath)
	#showContours(contours, inputPath)
	convertedContours = convertContourCoordinates(contours)
	drawingTime = findDrawingTime(convertedContours)
	print("Drawing file " + inputPath)
	print(len(convertedContours), "contours were found")
	print("Drawing time will be approximately", drawingTime, "seconds ("+str(drawingTime/60)+" minutes)")
	tkDrawContours(contours)
	print("Opening up robot connection...")
	try:
		mmm = MMM("COM3")
	except:
		print("ERROR: Could not connect to robot.")
		return
	print("Resetting robot...", end="")
	mmm.reset()
	# Countdown while resetting
	countdown(timeStepBetweenContours,"Resetting robot...","Done resetting robot")
	contourNumber = 1
	for contour in convertedContours:
		# Setup for each contour
		print("Drawing contour", contourNumber)
		firstPoint = contour[0]
		moveBetweenContours(mmm, firstPoint)
		for point in contour:
			print(point, end=" ")
			goTo(mmm, point)
			time.sleep(timeStep)
		contourNumber += 1
	print("Cleaning up...")
	mmm.reset()
	print("Done!")

def countdown(n,msg,endmsg):
	for countdown in range(n, 0, -1):
		print("\r" + msg + " " + str(countdown), end=" ")
		time.sleep(1)
	print("\r" + endmsg)

def goTo(mmm, point):
	# Takes a (theta, h) coordinate point and directs the robot's hand to it
	theta = point[0]
	h = point[1]
	mmm.setLeftGrippers(theta,0,0,0,0)
	mmm.extendArms(h/1000,0)
	mmm.update()

def moveBetweenContours(mmm, firstPoint):
	# Lift up arm
	mmm.rotateElbows(0,-90)
	# Go to first point
	goTo(mmm, firstPoint)
	countdown(timeStepBetweenContours, "Going to first point...", "Done going to first point")
	# Set down arm
	mmm.rotateElbows(-4,-90)
	mmm.update()
	time.sleep(1)


# Run
draw(inputPath)