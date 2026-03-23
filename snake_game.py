import maths
import random 
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1024)

detector = HandDetector(detectionCon = 0.8, maxHands = 1)

class SnakeGame :
    def __init__(self, pathfood):
        pass