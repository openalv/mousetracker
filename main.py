import imutils
import cv2
import numpy as np
import argparse
from collections import deque
from simple_pid import PID

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default = 64)
args = vars(ap.parse_args())

#Constans
title= "Mouse Tracking with Kalman Filter"
height = 600
width = 800
grey = 150
colorMouse = (64, 255, 255)

traceMouse = deque(maxlen = args["buffer"])

#Frame creation
frame = np.ones((height,width,3),np.uint8) * grey

def mouseMove(event, x, y, s, p):
    global frame, current_measurement
    current_measurement = np.array([[np.float32(x)], [np.float32(y)]])
    pointMouse = current_measurement[0], current_measurement[1]
    frame = np.ones((height,width,3),np.uint8) * grey

    cv2.circle(frame, pointMouse, 10, colorMouse, -1)
    traceMouse.appendleft(pointMouse)

   # loop over the set of tracked points
    for i in range(1, len(traceMouse)):
        # if either of the tracked points are None, ignore
	# them
        if traceMouse[i - 1] is None or traceMouse[i] is None:
            continue
	# otherwise, compute the thickness of the line and
	# draw the connecting lines
        thickness1 = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        thickness2 = 1      
        cv2.line(frame, traceMouse[i - 1], traceMouse[i], (0, 0, 255), thickness2)
    return

cv2.namedWindow(title)
cv2.setMouseCallback(title, mouseMove)

while True:
 
    cv2.imshow(title,frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
