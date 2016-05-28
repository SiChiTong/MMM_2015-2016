# import the necessary packages
from collections import deque
from MMM import MMM
import numpy as np
import argparse
import imutils
import cv2
import sys
import time
import json
import serial
import pygame

mmm = MMM('COM5');

#initial position of shoulder and elbow
rightShoulder = 100
rightElbow = -60

#initial pose
mmm.setWheelVelocity(0,0)
mmm.rotateShoulders(100, rightShoulder)
mmm.rotateElbows(-60, rightElbow)
mmm.extendArms(0,0)
mmm.setLeftGrippers(0,0,0,0,0)
mmm.setRightGrippers(0,0,0,0,0)
mmm.update(); 

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of red target in HSV
# then initialize the list of tracked points
redLower = (0, 75, 75)
redUpper = (200, 250, 250)
pts = deque(maxlen=args["buffer"])

# if a video not given, get webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# else get video
else:
	camera = cv2.VideoCapture(args["video"])

camera.set(3, 320)
camera.set(4, 240)
#get width and height
width = 640
height = 480

#initialize variables
#angle of right gripper
angle = 180
#initialize tracking boolean
track = False
#counter for mmm update
update = 0
#margin on x-axis
margin = width/10

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break
 
	# resize the frame, blur it, and convert it to the HSV
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for red, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, redLower, redUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the circle
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
 
	#initial wheel speeds
	leftWheelSpeed = 0
	rightWheelSpeed = 0

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw circle and center
			x2, y2 = center
			# if the circle is in the center of the screen, make it black
			if (x2 > width/2-radius and x2<width/2+radius and y2>height/2-radius and y2<height/2+radius):
				cv2.circle(frame, center, 5, (0, 0, 0), -1)
				cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 0, 0), 2)

			#otherwise, yellow with red center
			else:
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)

			#with offset - robot's gun is lower and farther to the right than webcam
			xOffset = x2 - margin
			yOffset = y2 - margin

			#translate the center to robot arm position
			rightShoulder = mmm.translate(640-xOffset, 0, 640, 50, 120)
			rightElbow = mmm.translate(yOffset, 0, 480, -60, 60)
			
			#rotate the arm
			mmm.rotateShoulders(100, rightShoulder)
			mmm.rotateElbows(-60, -rightElbow)
			

			# whether target is moving offscreen to the left
			# if center<=margin:
			# 	leftWheelSpeed = -0.18
			# 	rightWheelSpeed = 0.18
			
			# #target is moving offscreen to the right
			# elif center>=width-margin:
			# 	rightWheelSpeed = -0.18
			# 	leftWheelSpeed = 0.18

	# mmm.setWheelVelocity(leftWheelSpeed, rightWheelSpeed)

	# update the points queue
	pts.appendleft(center)

	#tracking switch
	key = cv2.waitKey(1) & 0xFF
	if key == ord('t'):
		track = not track
	if track == True:
		# loop over the set of tracked points
		for i in xrange(1, len(pts)):
			# if either of the tracked points are None, ignore
			# them
			if pts[i - 1] is None or pts[i] is None:
				continue

			# otherwise, compute the thickness of the line and
			# draw the connecting lines
			thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
			cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	# key = cv2.waitKey(1) & 0xFF

	#update counter
	update += 1

	#only update the right grippers after 50 frames
	if update == 50:
		if(angle == 180):  angle = 90
		elif(angle == 90):  angle = 180
		mmm.setRightGrippers(angle, 180, 180, 180, 180)
		update = 0
		
	#update everything else after 5 frames
	if update % 5:
		mmm.update()

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()