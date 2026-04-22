# Gesture-Based-Math-Solver
A real-time hand gesture calculator using OpenCV and MediaPipe. Perform arithmetic operations (+, -, *, /) and input numbers using finger gestures detected via webcam — no keyboard needed.  Tech: Python · OpenCV · MediaPipe · NumPy


## 🚀 Features

- Detect hand gestures in real-time via webcam
- Input numbers (0–9) using finger counts across two hands
- Perform arithmetic: Addition, Subtraction, Multiplication, Division
- Delete last character, clear screen, or exit — all with gestures
- Live expression and result display on screen

---

## 🖐️ Gesture Guide

| Gesture | Action |
|--------|--------|
| 1 finger (one hand) | Input digit |
| Both index fingers close together | Exit |
| 1 + 2 fingers | Subtraction (-) |
| 1 + 3 fingers | Multiplication (*) |
| 1 + 4 fingers | Division (/) |
| 1 + 1 fingers (apart) | Addition (+) |
| 2 + 2 fingers | Delete last character |
| Both fists (0+0) | Evaluate (=) |
| All fingers open (5+5) | Clear screen |
| Combined count 6–9 | Input digit 6–9 |

---

## 🛠️ Tech Stack

- **Python** 3.x
- **OpenCV** - webcam feed and display
- **MediaPipe** - hand landmark detection
- **NumPy** - distance calculations

---
