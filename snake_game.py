import math
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
        self.point = [] # all point of snake 
        self.length = [] # distance between each point 
        self.currentlength = 0
        self.allowedlength = 150 #max length
        self.prevhead = 0,0 

        self.imgfood = cv2.imread(pathfood ,cv2.IMREAD_UNCHANGED)
        self.hfood , wfood,_ = self.imgfood.shape
        self.foodpoint = 0,0
        self.randomFoodLocation()
        self.score = 0
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodpoint = random.randint(100,400),random.randint(100,400)

    def update(self, imgMain , currentHead):
        if self.gameOver:
            cvzone.putTextReact(imgMain, "Game Over", [300/2,400/2],scale= 2, thickness = 3, offset = 10)
            cvzone.putTextReact(imgMain, f"Your Score :{self.score}", [300/2,400/2],scale= 2, thickness = 3, offset = 10)

        else :
            px,py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentlength += distance
            self.prevhead = cx , cy

            if self.currentlength > self.allowedlength:
                for i,length in enumerate(self.lengths):
                    self.currentlength -=length
                    self.points.pop(i)
                    self.length.pop(i)
                    if self.currentlength < self.allowedlength:
                        break
                
            # checks if snake ate the food 
            rx,ry = self.foodpoint
            if rx - self.wfood // 2 < cx < rx + self.wfood//2 and \
                ry - self.hfood//2 < cy < ry + self.hfood//2:

                self.randomFoodLocation()
                self.allowedlength +=20
                self.score += 1
                print(self.score)

            #Draw Snake
            if self.points:
                for i.point in enumerate(self.points):
                    if i!=0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i],(0,0,255), 20 )
                    cv2.circle(imgMain, self.points[-1],20,(0,255,0),cv2.FILLED)

            #Draw Food
                
