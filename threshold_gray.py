# threshold_gray.py
# This program uses thresholding to track a ball.
# It demonstrates the use of gray scale image and Hough Circle detection.

import cv2
import numpy as np
import os
import Tkinter as Tk
# Define some global variables
# initial filter values.
# these will be changed using trackbars
# Some boolean variables for different functionality within this  program
DEBUG = 0
# default capture width and height
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
DP = 1
MAX_DP = 20
MIN_DIST = 100 
PARAM1 = 50
MAX_PARAM1 = 100
PARAM2 = 30
MAX_PARAM2 = 100 
MIN_RADIUS = 5
MAX_RADIUS = 100 
DP_TEXT = "DP = " + str(DP) + "\n" 
DIST_TEXT = " MIN_DIST = " + str(MIN_DIST) + "\n" 
PARAM_TEXT = "PARAM1 = " + str(PARAM1) + " PARAM2 = " + str(PARAM2) + "\n"
R_TEXT = "MIN_RADIUS = " + str(MIN_RADIUS) + " MAX_RADIUS = " + str(MAX_RADIUS) + "\n"
#EAP LEFT OFF HERE TRYING TO GET TK WINDOW TO UPDATE
root = Tk.Tk()
root.title("Slider Values")
ALL_TEXT = Tk.StringVar()
ALL_TEXT.set(DP_TEXT + DIST_TEXT + PARAM_TEXT + R_TEXT)
label = Tk.Label(root, textvariable=ALL_TEXT).pack()
# max number of objects to be detected in frame
MAX_NUM_OBJECTS=50
# minimum and maximum object area
MIN_OBJECT_AREA = 20*20
MAX_OBJECT_AREA = FRAME_HEIGHT*FRAME_WIDTH/1.5
# names that will appear at the top of each window
windowName = "Original Image"
windowName2 = "Gray Image"
windowName3 = "After Morphological Operations"
trackbarWindowName = "Trackbars"


def on_trackbar(message):
# This function gets called whenever a
# trackbar position is changed
    global DP 
    global MIN_DIST 
    global PARAM1 
    global PARAM2 
    global MIN_RADIUS 
    global MAX_RADIUS 
    global ALL_TEXT
    DP_NEW = cv2.getTrackbarPos("DP", trackbarWindowName)
    MIN_DIST_NEW = cv2.getTrackbarPos("MIN_DIST", trackbarWindowName)
    PARAM1_NEW = cv2.getTrackbarPos("PARAM1", trackbarWindowName)
    PARAM2_NEW = cv2.getTrackbarPos("PARAM2", trackbarWindowName)
    MIN_RADIUS_NEW = cv2.getTrackbarPos("MIN_RADIUS", trackbarWindowName)
    MAX_RADIUS_NEW = cv2.getTrackbarPos("MAX_RADIUS", trackbarWindowName)
    if(DEBUG):
     if(DP_NEW != DP and DEBUG == 1 ):
      print "DP was " + str(DP) + " DP now set to " + str(DP_NEW) +"\n"
    if(DEBUG):
     if(MIN_DIST_NEW != MIN_DIST and DEBUG == 1 ):
      print "MIN_DIST was " + str(MIN_DIST) + " MIN_DIST now set to " + str(MIN_DIST_NEW) +"\n"
     if(PARAM1_NEW != PARAM1 and DEBUG == 1 ):
      print "PARAM1 was " + str(PARAM1) + " PARAM1 now set to " + str(PARAM1_NEW) +"\n"
    if(DEBUG):
     if(PARAM2_NEW != PARAM2 and DEBUG == 1 ):
      print "PARAM2 was " + str(PARAM2) + " PARAM2 now set to " + str(PARAM2_NEW) +"\n"
     if(MIN_RADIUS_NEW != MIN_RADIUS and DEBUG == 1 ):
      print "MIN_RADIUS was " + str(MIN_RADIUS) + " MIN_RADIUS now set to " + str(MIN_RADIUS_NEW) +"\n"
    if(DEBUG):
     if(MAX_RADIUS_NEW != MAX_RADIUS and DEBUG == 1 ):
      print "MAX_RADIUS was " + str(MAX_RADIUS) + " MAX_RADIUS now set to " + str(MAX_RADIUS_NEW) +"\n"
    DP = DP_NEW
    MIN_DIST = MIN_DIST_NEW
    PARAM1 = PARAM1_NEW
    PARAM2 = PARAM2_NEW
    MIN_RADIUS = MIN_RADIUS_NEW
    MAX_RADIUS = MAX_RADIUS_NEW
    H_TEXT = "DP = " + str(DP) + " MIN_DIST = " + str(MIN_DIST) + "\n" 
    S_TEXT = "PARAM1 = " + str(PARAM1) + " PARAM2 = " + str(PARAM2) + "\n"
    V_TEXT = "MIN_RADIUS = " + str(MIN_RADIUS) + " MAX_RADIUS = " + str(MAX_RADIUS) + "\n"
    ALL_TEXT.set(H_TEXT + S_TEXT + V_TEXT) 

def createTrackbars(name):
# create window for trackbars

    cv2.namedWindow(name,0)
# create trackbars and insert them into window
# 3 parameters are: the address of the variable that is changing when the trackbar is moved(eg.H_LOW),
# the max value the trackbar can move (eg. H_HIGH), 
# and the function that is called whenever the trackbar is moved(eg. on_trackbar)
#                                   ---->    ---->     ---->      
    cv2.createTrackbar( "DP", name, DP, MAX_DP, on_trackbar )
    cv2.createTrackbar( "MIN_DIST", name, MIN_DIST, FRAME_WIDTH, on_trackbar )
    cv2.createTrackbar( "PARAM1", name, PARAM1, MAX_PARAM1, on_trackbar )
    cv2.createTrackbar( "PARAM2", name, PARAM2, MAX_PARAM2, on_trackbar )
    cv2.createTrackbar( "MIN_RADIUS", name, MIN_RADIUS, MAX_RADIUS, on_trackbar )
    cv2.createTrackbar( "MAX_RADIUS", name, MAX_RADIUS, MAX_RADIUS, on_trackbar )



#######################################################
# All code below here is main                         #
#######################################################
#on_trackbar(MAX_NUM_OBJECTS)
capWebcam = cv2.VideoCapture(0) # declare a VideoCapture object and associate to webcam, 0 => use 1st webcam
print "default resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
capWebcam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)              # change resolution to 320x240 for faster processing
capWebcam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
print "updated resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
if capWebcam.isOpened() == False:                           # check if VideoCapture object was associated to webcam successfully
   print "error: capWebcam not accessed successfully\n\n"          # if not, print error message to std out
   os.system("pause")                                              # pause until user presses a key so user can see error message
createTrackbars(trackbarWindowName)
while cv2.waitKey(1) != 27 and capWebcam.isOpened():  # until the Esc key is pressed or webcam connection is lost
      blnFrameReadSuccessfully, imgOriginal = capWebcam.read()            # read next frame
      if not blnFrameReadSuccessfully or imgOriginal is None:             # if frame was not read successfully
            print "error: frame not read from webcam\n"                     # print error message to std out
            os.system("pause")                                              # pause until user presses a key so user can see error message
            break                                                           # exit while loop (which exits program)
      imgBlur = cv2.medianBlur(imgOriginal,5)
      imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
      #circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT,DP,MIN_DIST) 
      circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT,DP,MIN_DIST, param1=PARAM1,param2=PARAM2,minRadius=MIN_RADIUS,maxRadius=MAX_RADIUS) 
      #circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT,1,100, param1=50,param2=30,minRadius=5,maxRadius=100) 
      if circles is not None:  # this line is necessary to keep program from crashing on next line if no circles were found
         for circle in circles[0]:                           # for each circle
          x, y, radius = circle                                                                       # break out x, y, and radius
          print "ball position x = " + str(x) + ", y = " + str(y) + ", radius = " + str(radius)       # print ball position and radius
          cv2.circle(imgOriginal, (x, y), 3, (0, 255, 0), -1)           # draw small green circle at center of detected object
          cv2.circle(imgOriginal, (x, y), radius, (0, 0, 255), 3)                     # draw red circle around the detected object

      cv2.imshow(windowName2,imgGray);
      cv2.imshow(windowName,imgOriginal);
