# Hand_gesture_snake_game

# 🐍 Hand Gesture Controlled Snake Game

🚀 An interactive Snake Game controlled using real-time hand gestures powered by Computer Vision.

---

## 🎥 Demo
![Demo](demo.gif)

---

## 🧠 Features

- ✋ Real-time hand gesture control using webcam  
- 🎮 Smooth snake movement using index finger tracking  
- 🍎 Dynamic food spawning system  
- 💥 Self-collision detection (Game Over logic)  
- 🔄 Restart functionality (Press 'R')  
- ⚡ Optimized for low-latency performance  
- 📊 Real-time score display  

---

## 🧪 Tech Stack

- **Python**
- **OpenCV**
- **cvzone**
- **MediaPipe**
- **NumPy**

---

## 🏗️ How It Works

- Uses **MediaPipe Hand Tracking** to detect hand landmarks  
- Tracks index finger tip (landmark 8) for snake movement  
- Calculates distance between points to simulate snake body  
- Detects collision using polygon test  
- Overlays food using PNG transparency  

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/snake-game-cv.git
cd snake-game-cv
pip install -r requirements.txt
