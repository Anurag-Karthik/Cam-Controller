import cv2
import os
import mediapipe as mp

signName = ''
signImgsPath = f'O:/CamController/Data/Images/{signName}'
noOfImgs = os.listdir(signImgsPath)

# Fetching necessary Modules from complete mediapipe library
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils 

#Initializing
for index in range(0, noOfImgs):
