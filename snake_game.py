import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)


class SnakeGame:
    def __init__(self, pathfood):
        self.points = []
        self.lengths = []
        self.currentLength = 0
        self.allowedLength = 150
        self.prevHead = (0, 0)

        self.imgFood = cv2.imread(pathfood, cv2.IMREAD_UNCHANGED)
        self.imgFood = cv2.resize(self.imgFood, (50, 50))

        self.hFood, self.wFood, _ = self.imgFood.shape

        self.foodPoint = (0, 0)
        self.randomFoodLocation()

        self.score = 0
        self.gameOver = False
        self.paused = False

        # Stability
        self.frameCount = 0
        self.lastHead = None
        self.missingFrames = 0

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):

        self.frameCount += 1

        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [400, 300],
                               scale=3, thickness=3)
            return imgMain

        if self.paused:
            cvzone.putTextRect(imgMain, "Paused", [500, 300],
                               scale=3, thickness=3)
            return imgMain

        cx, cy = currentHead

        if self.prevHead == (0, 0):
            self.prevHead = (cx, cy)

        px, py = self.prevHead

        # Add new point
        self.points.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.lengths.append(distance)
        self.currentLength += distance
        self.prevHead = (cx, cy)

        # Limit snake length
        if self.currentLength > self.allowedLength:
            for i, length in enumerate(self.lengths):
                self.currentLength -= length
                self.points.pop(i)
                self.lengths.pop(i)
                if self.currentLength < self.allowedLength:
                    break

        # Food collision
        rx, ry = self.foodPoint
        if (rx - self.wFood // 2 < cx < rx + self.wFood // 2 and
                ry - self.hFood // 2 < cy < ry + self.hFood // 2):

            self.randomFoodLocation()
            self.allowedLength += 40
            self.score += 1

        # Draw snake
        if self.points:
            for i, point in enumerate(self.points):
                if i != 0:
                    cv2.line(imgMain, tuple(self.points[i - 1]),
                             tuple(point), (0, 0, 255), 20)

            cv2.circle(imgMain, tuple(self.points[-1]),
                       20, (0, 255, 0), cv2.FILLED)

        # Draw food
        imgMain = cvzone.overlayPNG(
            imgMain,
            self.imgFood,
            (rx - self.wFood // 2, ry - self.hFood // 2)
        )

        cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80],
                           scale=2, thickness=2)

        # 🔥 ACCURATE COLLISION DETECTION
        if len(self.points) > 20:
            head = np.array(self.points[-1])

            for i in range(0, len(self.points) - 10, 2):  # skip nearby + optimize
                body = np.array(self.points[i])

                dist = np.linalg.norm(head - body)

                if dist < 20:  # collision threshold
                    self.gameOver = True
                    break

        return imgMain


# Initialize
game = SnakeGame("red_dot.png")
startGame = False

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    # Start screen
    if not startGame:
        cvzone.putTextRect(img, "Press SPACE to Start", [300, 300],
                           scale=2, thickness=3)

    else:
        if hands:
            lmList = hands[0]['lmList']
            fingers = detector.fingersUp(hands[0])

            pointIndex = lmList[8][0:2]
            game.lastHead = pointIndex
            game.missingFrames = 0

            # Pause
            if fingers == [1, 1, 1, 1, 1]:
                game.paused = True

            # Play
            elif fingers == [0, 1, 0, 0, 0]:
                game.paused = False

        # Smooth tracking
        if game.lastHead is not None:
            game.missingFrames += 1

            if game.missingFrames < 10:
                img = game.update(img, game.lastHead)
            else:
                game.paused = True

    cv2.imshow("Snake Game", img)

    key = cv2.waitKey(1)

    if key == 32:  # SPACE
        startGame = True

    if key == ord('r'):
        game = SnakeGame("red_dot.png")
        startGame = False

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()