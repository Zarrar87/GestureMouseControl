# GestureMouseControl 🎯🖐️

Control your mouse using only your hand gestures via your webcam, powered by OpenCV, MediaPipe, and PyAutoGUI.

## 📌 Overview

This project uses real-time hand tracking to:
- **Move the mouse cursor** using your index fingertip.
- **Right-click** using a 👍 thumbs-up gesture.
- **Left-click** using an index-only gesture.

No keyboard or mouse needed — just your hand and a webcam.

---

## 🧠 Features

| Gesture              | Action           |
|----------------------|------------------|
| Index finger up      | Move mouse       |
| Thumbs up            | Right-click      |
| Index only up        | Left-click       |

Each gesture is detected using **MediaPipe’s 21-point hand landmark system**, and the cursor is controlled using **PyAutoGUI** to match your fingertip position.

---

## 🎥 Demo

> **

---

## 🛠 Requirements

Install dependencies via pip
pip install opencv-python mediapipe pyautogui:

```
pip install opencv-python mediapipe pyautogui

