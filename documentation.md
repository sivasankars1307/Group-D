# 📘 Project Documentation

## Project Title
**Hand Gesture–Based Microphone Volume Control System**

---

## 1. Introduction

This project implements a **real-time, touchless microphone control system** using hand gestures captured from a webcam. The system allows a user to **mute/unmute** and **adjust microphone volume** by changing the distance between the thumb and index finger.

The motivation behind this project is to provide a **hands-free interaction mechanism**, useful in scenarios such as online meetings, presentations, accessibility applications, and hygienic human–computer interaction.

---

## 2. Problem Statement

Traditional microphone control requires:
- Physical interaction with keyboard or UI controls
- Context switching during meetings or presentations
- Accessibility accommodations for users with motor limitations

**Objective:**
Design a system that enables **intuitive, gesture-based microphone control** using computer vision without additional hardware.

---

## 3. System Overview

The system integrates:
- Computer Vision for hand detection
- Gesture analysis for intent recognition
- Operating System–level APIs for microphone control
- A real-time interactive user interface

The solution operates entirely on the client machine and processes video frames in real time.

---

## 4. Architecture Description

### 4.1 High-Level Architecture

**Input → Processing → Decision → Action → Feedback**

Components:
1. Webcam (video input)
2. OpenCV (frame acquisition & preprocessing)
3. MediaPipe Hands (21 landmark detection)
4. Gesture Analysis Module (ratio-based computation)
5. Decision Engine (mute vs volume control)
6. PyCAW (Windows Core Audio API)
7. Streamlit UI (visual feedback & controls)

This modular structure ensures separation of concerns and easy extensibility.

---

## 5. Gesture Recognition Logic

### 5.1 Landmark Selection

The following landmarks are used:
- Thumb Tip (ID 4)
- Index Finger Tip (ID 8)
- Wrist (ID 0)
- Middle Finger MCP (ID 9)

These landmarks provide a stable geometric reference for gesture analysis.

### 5.2 Scale-Invariant Ratio Calculation

Instead of using raw pixel distance, a **normalized ratio** is computed:

```
Pinch Ratio = Distance(Thumb Tip, Index Tip)
              --------------------------------
              Distance(Wrist, Middle MCP)
```

**Why this matters:**
- Prevents false volume changes when the hand moves closer/farther from the camera
- Ensures consistent behavior across users and hand sizes

---

## 6. Decision Logic

| Condition | Action |
|---------|--------|
| Ratio ≤ 0.15 | Microphone muted |
| Ratio > 0.15 | Microphone unmuted and volume adjusted |

Volume is mapped linearly from the ratio range `[MIN_RATIO, MAX_RATIO]` to `[0%, 100%]`.

A smoothing step is applied to prevent jitter.

---

## 7. Processing Flow

1. Initialize Streamlit UI
2. Load MediaPipe hand model (cached)
3. User starts camera
4. Capture frame from webcam
5. Convert frame to RGB
6. Detect hand landmarks
7. Compute pinch ratio
8. Decide mute or volume adjustment
9. Apply microphone control via PyCAW
10. Update UI metrics and annotated video
11. Repeat until camera stopped

---

## 8. User Interface Description

### 8.1 Sidebar
- Camera index selection
- Manual volume increase (+20%)
- Manual volume decrease (−20%)

### 8.2 Main Panel
- Start/Stop camera control
- Live camera feed with landmark overlay
- Real-time microphone volume indicator
- Gesture ratio metric
- Mute/unmute status message

The UI is styled using **custom CSS** inspired by Apple’s design language for clarity and aesthetics.

---

## 9. Technology Stack

- **Python** – Core programming language
- **Streamlit** – Web-based UI framework
- **MediaPipe** – Hand landmark detection
- **OpenCV** – Video capture and processing
- **NumPy** – Mathematical operations
- **PyCAW** – Windows microphone control
- **COM Interfaces** – Low-level OS interaction

---

## 10. Platform Constraints

- Supported OS: **Windows only**
- Reason: PyCAW depends on Windows Core Audio APIs
- Webcam and microphone must be available and set as default devices

---

## 11. Limitations

- Only one hand is supported at a time
- Performance depends on lighting conditions
- Background clutter may affect hand detection accuracy
- No gesture personalization per user

---

## 12. Future Enhancements

- Multi-hand gesture support
- User-calibrated gesture thresholds
- Cross-platform audio abstraction
- Gesture-based push-to-talk
- Desktop (PyQt) or executable (.exe) deployment

---

## 13. Conclusion

This project demonstrates the integration of **computer vision, real-time processing, and system-level programming** to solve a practical interaction problem. The use of scale-invariant gesture analysis and OS-level audio control reflects engineering-level design rather than a prototype or toy implementation.

---

## 14. Academic Relevance

This project covers concepts from:
- Computer Vision
- Human–Computer Interaction (HCI)
- Operating Systems
- Software Architecture
- Real-Time Systems

It is suitable for **mini-projects, major projects, and technical evaluations**.

