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
mmm.extendArms(0,0.127)
mmm.setLeftGrippers(0,0,0,0,0)
mmm.setRightGrippers(0,0,0,0,0)
mmm.update(); 

# timeDelay = 1
# angle = 0
# while(True):
mmm.setRightGrippers(180, 180, 180, 180, 180)
mmm.update()
# time.sleep(1.0);
	# mmm.setRightGrippers(90, 180, 180, 180, 180)
	# mmm.update()
	# time.sleep(1.0);
	# mmm.setRightGrippers(180, 180, 180, 180, 180)
	# mmm.update()
	# time.sleep(1.0);
	