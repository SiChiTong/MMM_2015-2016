from __future__ import print_function, division
import PIL.Image
import math
import cv2
import numpy
import serial
from MMM import MMM
from Tkinter import *
from ttk import *
import tkFileDialog
import tkMessageBox

# Global Resources
root = Tk()
class Struct(object): pass
data = Struct()
data.consoleText = ""
# Global Parameters
data.filePath = "" # Make sure to load square images in RGB format
data.webcamImage = 0
data.drawWidth, data.drawHeight = (100,100)
data.canvasSize = 1000
r = 50 # mm radius of the servo motion
data.timeStep = 250 # milliseconds, probably don't go faster than 0.25
data.resetTime = 20000 # milliseconds, based on experiments for speed and max distance between contours
data.animationDelay = 10 # milliseconds, for animation
data.linearSpeed = .127/24.38 # meters/second
data.liftArmTime = 500 # milliseconds
data.elbowDrawingAngle = -4 # degrees
data.elbowLiftAngle = -2 # degrees

# TODO
# Change color of Preview and Draw buttons
# Add settings window to change drawing settings
# Make contour transitions more efficient

####################################################################################################
# User Interface Stuff
####################################################################################################

def mainWindow():
	root.title("DrawBot")
	root.state("zoomed") # Maximize the window

	# Construct objects
	data.loadFileButton = Button(root, text="Load image from file", command=loadFile)
	data.filePathLabel = Label(root, text="Input status: no input selected")
	data.webcamButton = Button(root, text="Take picture on webcam", command=getWebcamPicture)
	data.previewButton = Button(root, text="Preview", state=DISABLED, command=previewDrawing)
	data.drawButton = Button(root, text="Draw", state=DISABLED, command=draw)
	data.canvas = Canvas(root, width=data.canvasSize, height=data.canvasSize, background="white")
	data.textBox = Text(root, bg="black", fg="white", font="Consolas")#, state=DISABLED)

	# Layout
	padding = 5
	data.loadFileButton.grid(row=0, column=0, padx=padding, pady=padding, sticky="NSEW")
	data.filePathLabel.grid(row=0, column=1, rowspan = 2, padx=padding, pady=padding, sticky="NS")
	data.webcamButton.grid(row=1, column=0, padx=padding, pady=padding, sticky="NSEW")
	data.drawButton.grid(row=2, column=1, padx=padding, pady=padding, sticky="NSEW")
	data.previewButton.grid(row=2, column=0, padx=padding, pady=padding, sticky="NSEW")
	data.canvas.grid(row=3, column=0, padx=padding, pady=padding)
	data.textBox.grid(row=3, column=1, padx=padding, pady=10, sticky="NSEW")

	root.grid_columnconfigure(0, weight=1)
	root.grid_columnconfigure(1, weight=1)
	root.grid_rowconfigure(0, weight=1)
	root.grid_rowconfigure(1, weight=1)
	root.grid_rowconfigure(2, weight=1)
	root.grid_rowconfigure(3, weight=0)

	# Key Input
	root.bind("<Key>", lambda event: tkKeyPressed(event))

	# Loop
	root.mainloop()


def loadFile():
	data.filePath = tkFileDialog.askopenfilename()
	if data.filePath != "":
		try:
			data.imWidth, data.imHeight = PIL.Image.open(data.filePath).size
			data.filePathLabel.config(text = "Input status: using file " + str(data.filePath))
			data.previewButton.config(state=NORMAL)
			data.drawButton.config(state=NORMAL)
			data.webcamImage = 0
		except:
			tkMessageBox.showinfo("Error", "Could not load image from " + data.filePath + ".")
			data.filePath = ""

def getWebcamPicture():
	camera = cv2.VideoCapture(1)
	cv2.namedWindow("Press Space to take a picture", cv2.WINDOW_NORMAL)
	cv2.resizeWindow("Press Space to take a picture", 1080, 1080)
	# Actual size is 360x640
	while True:
		ret, frame = camera.read()
		#croppedFrame = frame[y1:y2, x1:x2]
		croppedFrame = frame[0:360, 140:500]
		cv2.imshow("Press Space to take a picture", croppedFrame)
		if cv2.waitKey(1) == 32: # space bar
			data.webcamImage = cv2.resize(croppedFrame, (200, 200))
			data.imHeight, data.imWidth = (data.webcamImage.shape[0], data.webcamImage.shape[1])
			break
	camera.release()
	cv2.destroyAllWindows()
	data.filePathLabel.config(text = "Input status: using webcam photo")
	data.previewButton.config(state=NORMAL)
	data.drawButton.config(state=NORMAL)
	data.filePath = ""


def printConsole(text, end="\n"):
	data.consoleText += text + end
	#data.textBox.config(state=NORMAL)
	#data.textBox.delete("1.0",END)
	data.textBox.insert(END, text + end)
	print("Printed a line: " + text, end=end)
	#data.textBox.config(state=DISABLED)


####################################################################################################
# OpenCV Stuff
####################################################################################################

#def invertImage(image):
#def flipImage(image):

def openImage(filePath):
	# Opens an image with OpenCV
	inputImage = cv2.imread(filePath)
	return inputImage

def applyThreshold(inputImage):
	# Apply a threshold to the image
	imgray = cv2.cvtColor(inputImage,cv2.COLOR_RGB2GRAY)
	ret, threshold = cv2.threshold(imgray,0,255,cv2.THRESH_OTSU)
	return threshold

def getContours():
	# Finds the contours of a binary image, returns a numpy array of contours
	if data.filePath != "":
		inputImage = openImage(data.filePath)
	elif type(data.webcamImage) != int:
		inputImage = data.webcamImage
	threshold = applyThreshold(inputImage)
	im2, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # RETR_LIST or RETR_EXTERNAL
	return contours


####################################################################################################
# Coordinate System Stuff
####################################################################################################

def radiansToDegrees(theta):
	return theta * 180 / math.pi

def resizeImage(coordinates):
	# Resizes a larger square image to a 100x100 square image
	x = coordinates[0]
	y = coordinates[1]
	return (x/data.imWidth*data.drawWidth, y/data.imHeight*data.drawHeight)

def transformCoordinates(coordinates):
	# Shifts a 
	x = coordinates[0]
	y = coordinates[1]
	return (x-data.drawWidth/2, data.drawHeight-y)

def convertCoordinateSystem(coordinates):
	# returns theta in degrees 0-180 and h in mm
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


####################################################################################################
# Animate Coordinate Drawing
####################################################################################################

def tkKeyPressed(event):
	if event.keysym == "Up":
		data.animationDelay //= 10
	elif event.keysym == "Down" and data.animationDelay < 1000:
		if data.animationDelay == 0:
			data.animationDelay = 1
		else:
			data.animationDelay *= 10

def previewDrawing():
	contours = getContours()
	data.canvas.delete("all")
	contourNumber = 1
	pointerRadius = int(data.canvasSize/100)
	for contour in range(len(contours)):
		for point in range(len(contours[contour])):
			x1 = contours[contour][point][0][0]/data.imWidth*data.canvasSize
			y1 = contours[contour][point][0][1]/data.imHeight*data.canvasSize
			x2 = contours[contour][(point+1)%len(contours[contour])][0][0]/data.imWidth*data.canvasSize
			y2 = contours[contour][(point+1)%len(contours[contour])][0][1]/data.imHeight*data.canvasSize
			data.canvas.create_line(x1, y1, x2, y2, fill="black")
			pointer = data.canvas.create_oval(x2-pointerRadius, y2-pointerRadius, x2+pointerRadius, y2+pointerRadius, fill="red", outline="")
			speed = data.canvas.create_text((5,0), anchor="nw", text="Press Up or Down to change speed")
			root.update()
			data.canvas.delete(pointer)
			data.canvas.delete(speed)
			root.after(data.animationDelay)
		contourNumber += 1



####################################################################################################
# Physical Drawing Stuff and Console Output
####################################################################################################

def findDrawingTime(convertedContours):
	# Returns estimated drawing time in seconds based on a contour array
	time = 0
	time += data.resetTime/1000
	time += getContourTimeStep([(0,0)], convertedContours[0])/1000
	for i in range(len(convertedContours)):
		contour = convertedContours[i]
		time += len(contour) * (data.timeStep/1000) + getContourTimeStep(convertedContours[i-1], convertedContours[i])/1000 + 2 * data.liftArmTime/1000
	return time

def draw():
	data.textBox.delete("1.0",END) # Clear console
	printConsole("Initializing...")
	contours = getContours()
	convertedContours = convertContourCoordinates(contours)
	drawingTime = findDrawingTime(convertedContours)
	if data.filePath != "":
		printConsole("Drawing file " + data.filePath)
	elif type(data.webcamImage) != int:
		printConsole("Drawing webcam photo")
	printConsole(str(len(convertedContours)) + " contours were found")
	printConsole("Drawing time will be approximately " + str(drawingTime) + " seconds ("+str(drawingTime/60)+" minutes)")
	printConsole("Opening up robot connection...")
	#previewDrawing() Causes errors?
	try:
		mmm = MMM("COM3")
	except:
		printConsole("ERROR: Could not connect to robot.")
		return # break out of the draw function
	printConsole("Resetting robot...", end=" ")
	mmm.reset()
	mmm.update()
	root.after(data.resetTime)
	printConsole("Done resetting robot.")
	contourNumber = 1 # Initialize contour counter
	for contour in convertedContours:
		# Setup for each contour
		printConsole("Drawing contour " + str(contourNumber))
		firstPoint = contour[0]
		moveBetweenContours(mmm, firstPoint)
		for point in contour:
			printConsole(str(point), end=" ")
			goTo(mmm, point)
			root.after(data.timeStep)
		contourNumber += 1
	printConsole("Cleaning up...", end=" ")
	mmm.reset()
	mmm.update()
	printConsole("Done!")

def goTo(mmm, point):
	# Takes a (theta, h) coordinate point and directs the robot's hand to it
	theta = point[0]
	h = point[1]
	mmm.setLeftGrippers(theta,0,0,0,0)
	mmm.extendArms(h/1000,0)
	mmm.update()

def moveBetweenContours(mmm, firstPoint):
	# Lift up arm
	mmm.rotateElbows(data.elbowLiftAngle,-90)
	mmm.update()
	root.after(data.liftArmTime)
	# Go to first point
	goTo(mmm, firstPoint)
	printConsole("Going to first point...", end=" ")
	root.after(data.contourTimeStep)
	printConsole("Done going to first point.")
	# Set down arm
	mmm.rotateElbows(data.elbowDrawingAngle,-90)
	mmm.update()
	root.after(data.liftArmTime)

def getContourTimeStep(contour1, contour2):
	# Returns time in seconds
	point1 = contour1[-1]
	point2 = contour2[0]
	h1 = point1[1]
	h2 = point2[1]
	distance = abs(h1-h2) / 1000 # in meters
	# time = distance/speed
	time = distance / data.linearSpeed
	return (time + 1) # +1 for safety
	#758.75 seconds before optimization
	#328.873731957 seconds after optimization


####################################################################################################
# Run
####################################################################################################
mainWindow()