from MMM import MMM
import sys
import time

class Position(object):

    def __init__(self, wheelVelocity, shoulders, elbows, arms, leftGrippers, rightGrippers):
        self.wheelVelocity = wheelVelocity
        self.shoulders = shoulders
        self.elbows = elbows
        self.arms = arms
        self.leftGrippers = leftGrippers
        self.rightGrippers = rightGrippers
        self.data = list(wheelVelocity) + list(shoulders) + list(elbows) + list(arms) + list(leftGrippers) + list(rightGrippers)

def stepFromTo(initial_position,final_position,steps=1):
    assert(len(initial_position.data) == len(final_position.data))
    length = len(initial_position.data)
    step = [0] * length
    current_position = [0] * length
    for i in xrange(length):
        step[i] = final_position[i] - initial_position[i]
    for step in xrange(steps):
        for j in xrange(length):
            current_position[j] = step[j] * (step + 1) / steps
        goTo(current_position)


def goTo(l):
    MMM.setWheelVelocity = (l[0],l[1])
    MMM.setShoulders = (l[2],l[3])
    MMM.setElbows = (l[4],l[5])
