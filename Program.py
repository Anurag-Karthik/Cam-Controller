import cv2
import os
import json
import mediapipe as mp
import numpy as np
import pyautogui as pc
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from math import sqrt

def distanceBetweenPoints(p1x, p1y, p2x, p2y):
    return sqrt(((p2x - p1x) * (p2x - p1x)) + ((p2y - p1y) * (p2y - p1y)))

def findMidPoint(p1x, p1y, p2x, p2y):
    return (((p1x + p2x)/2), ((p1y + p2y)/2))

def calculateAngle(p1x, p1y, p2x, p2y, p3x, p3y):
    radians = np.arctan2(p3y-p2y, p3x-p2x) - np.arctan2(p1y-p2y, p1x-p2x)
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

pc.FAILSAFE = False

#Initializing Camera
cam = cv2.VideoCapture(0)

#Obtaining PC Height and Width
pcScreenHeightWidth = pc.size()
pcScreenHeight = pcScreenHeightWidth[1]
pcScreenWidth = pcScreenHeightWidth[0]

#This is the variable which sets the minimum length between fingers for them to be considered as a pinch
fingerSpace = 0.05

#Initializing Necessary Mediapipe Models
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils

#mouseUp & mouseDown handling variables
isMouseDown = False

#prevCoordinates is used to Store previous CoOrdinates and caluculate relative position
prevCoordinates = []

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.2) as landmarker:
    while True:
        #Obtaining Frame from Camera
        ret, frame = cam.read()
        #Obtaining No.of Pixels in Camera Output which are later using to Scale Outputs obtained by various models
        camImgHeight = frame.shape[0]
        camImgWidth = frame.shape[1]
        #Cropping Image to get Hold of Corners
        # tenPerofCamWidth = int((10 * camImgWidth)/100)
        # tenPerofCamHeight = int((10 * camImgHeight)/100)
        # frame = frame[tenPerofCamWidth:(camImgWidth - tenPerofCamWidth), tenPerofCamHeight:(camImgHeight - tenPerofCamHeight)]
        if not ret:
            print("No Proper Input from Camera! Hence ignoring the processing.")
            continue

        #Processing using the Mediapipe Model
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = landmarker.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        #Checking for Hands
        if results.multi_hand_landmarks:
            #Converting Output into Usable Objects
            handLandmarks = []
            landmarks = str(results.multi_hand_landmarks[0]).replace("\n", "").split("landmark {")
            landmarks.pop(0)
            for landmark in landmarks:
                points = landmark.split('  ')
                handLandmarks.append({
                    'x': float(points[1].removeprefix('x: ')),
                    'y': float(points[2].removeprefix('y: '))
                })

            #8 & 4 are landmarks of Thumb and Index and are used to detect pinch and move mouse
            if(distanceBetweenPoints(handLandmarks[4]['x'], handLandmarks[4]['y'], handLandmarks[8]['x'], handLandmarks[8]['y']) <= fingerSpace):
                mouseCordinates = findMidPoint(handLandmarks[4]['x'], handLandmarks[4]['y'], handLandmarks[8]['x'], handLandmarks[8]['y'])
                if(prevCoordinates == []):
                    prevCoordinates = mouseCordinates
                    continue
                currentMouseX, currentMouseY = pc.position()
                # pc.moveTo((pcScreenWidth - (mouseCordinates[0] * pcScreenWidth)), (mouseCordinates[1] * pcScreenHeight))
                pc.moveTo((currentMouseX + ((mouseCordinates[0] - prevCoordinates[0]) * pcScreenWidth)), (currentMouseY + ((mouseCordinates[1] - prevCoordinates[1]) * pcScreenHeight)))
                prevCoordinates = mouseCordinates
            else:
                prevCoordinates = []

            #12 & 4 are landmarks of Thumb and Index and are used to perform Mouse Down and Up
            if(distanceBetweenPoints(handLandmarks[12]['x'], handLandmarks[12]['y'], handLandmarks[4]['x'], handLandmarks[4]['y']) <= fingerSpace):
                if isMouseDown == False:
                    pc.mouseDown()
                    isMouseDown = True
            else:
                if isMouseDown:
                    pc.mouseUp()
                    isMouseDown = False

            #16 & 4 are landmarks of Thumb and Index and are used to perform Right Click
            if(distanceBetweenPoints(handLandmarks[20]['x'], handLandmarks[20]['y'], handLandmarks[4]['x'], handLandmarks[4]['y']) <= fingerSpace):
                pc.click(button='right')

            #Drawing Landmarks
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS)
        else:
            print("No Hands")
                
        #Displaying the Image
        cv2.imshow('CamController', img)

        #Q set as the key for Quitting the Application
        if cv2.waitKey(1) & 0xFF == ord('Q'):
            break


#Releaseing accquired Camera before Terminating
cam.release()
cv2.destroyAllWindows()