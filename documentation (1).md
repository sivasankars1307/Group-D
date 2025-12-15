# 📘 Project Documentation

## Project Title
**Hand Gesture–Based Volume Control System**

---

## 1. Introduction

This project implements a **real-time, touchless microphone volume control system** using hand gestures captured via a webcam. By leveraging **computer vision** and **hand landmark detection**, the system allows users to mute/unmute and control microphone volume without physical interaction.

The project aligns with the Infosys SpringBoard curriculum and demonstrates applied knowledge of **Computer Vision, Human–Computer Interaction (HCI), Real-Time Systems, and OS-level programming**.

---

## 2. Problem Statement

Conventional microphone volume control requires physical interaction with hardware keys or on-screen controls, which:
- Interrupts workflow during meetings or presentations
- Is inconvenient in hands-busy scenarios
- Reduces accessibility for users with motor limitations

**Goal:**
Design and implement a **gesture-based, contactless microphone control system** using only a standard webcam and software techniques.

---

## 3. Objectives

- Detect and track human hand landmarks in real time
- Recognize pinch-based gestures using geometric analysis
- Map gestures to microphone volume levels smoothly
- Provide real-time visual feedback to the user
- Ensure robustness against hand depth variation

---

## 4. System Architecture

### 4.1 Architecture Diagram

📌 **Insert Image Here:** `architecture_diagram.png`

**Description:**  
The architecture diagram illustrates the end-to-end flow of data and control across system components:

1. **Webcam** captures live video frames
2. **OpenCV** handles frame acquisition and preprocessing
3. **MediaPipe Hands** detects 21 hand landmarks
4. **Gesture Logic Module** computes a scale-invariant pinch ratio
5. **Decision Engine** determines mute or volume adjustment
6. **PyCAW (Windows Core Audio API)** applies microphone control
7. **Streamlit UI** displays live video, metrics, and system status

This modular design ensures clear separation of concerns and real-time responsiveness.

---

## 5. Workflow / Flow Diagram

📌 **Insert Image Here:** `workflow_diagram.png`

### Execution Flow

1. Application starts and initializes UI
2. MediaPipe hand model is loaded (cached)
3. User starts the camera
4. Frame captured from webcam
5. Frame converted to RGB
6. Hand landmarks detected
7. Gesture ratio computed
8. Gesture classified (mute or volume control)
9. Microphone volume updated
10. UI metrics and video updated
11. Loop continues until user stops camera

---

## 6. Module Description

### 6.1 Webcam Input & Hand Detection Module
- Captures live video using OpenCV
- Uses MediaPipe Hands to detect 21 landmarks
- Operates in real time with low latency

### 6.2 Gesture Recognition & Distance Measurement Module
- Extracts key landmarks:
  - Thumb tip (ID 4)
  - Index tip (ID 8)
  - Wrist (ID 0)
  - Middle finger MCP (ID 9)
- Computes normalized pinch ratio to avoid depth-related errors

### 6.3 Volume Mapping & Control Module
- Maps gesture ratio to volume range (0–100%)
- Uses PyCAW to control Windows microphone
- Applies smoothing to prevent sudden jumps

### 6.4 User Interface & Feedback Module
- Displays live camera feed with landmark overlay
- Shows real-time microphone volume
- Indicates mute/unmute state
- Provides manual volume override buttons

---

## 7. Gesture Recognition Logic

### Scale-Invariant Formula

```
Pinch Ratio = Distance(Thumb Tip, Index Tip)
              --------------------------------
              Distance(Wrist, Middle MCP)
```

**Why this approach is used:**
- Prevents false volume changes when hand moves closer or farther from camera
- Ensures consistent behavior across users
- Improves system stability

---

## 8. Decision Logic

| Condition | Action |
|---------|--------|
| Ratio ≤ 0.15 | Microphone muted |
| Ratio > 0.15 | Volume adjusted dynamically |

Volume values are interpolated linearly and smoothed.

---

## 9. User Interface Description

### Sidebar
- Camera index selection
- Manual volume increase (+20%)
- Manual volume decrease (−20%)

### Main Panel
- Start/Stop camera control
- Live annotated video feed
- Gesture ratio metric
- Microphone volume indicator
- Mute/unmute status

The UI uses custom CSS inspired by Apple’s design guidelines for clarity and usability.

---

## 10. Technology Stack

- **Python**
- **Streamlit** – UI framework
- **MediaPipe** – Hand landmark detection
- **OpenCV** – Video processing
- **NumPy** – Mathematical operations
- **PyCAW** – Windows microphone control
- **COM Interfaces** – OS-level interaction

---

## 11. Platform Constraints

- Supported OS: **Windows only**
- Requires webcam and microphone
- Microphone must be set as default input device

---

## 12. Limitations

- Single-hand support only
- Performance affected by lighting conditions
- No per-user gesture calibration
- Background clutter may reduce accuracy

---

## 13. Future Enhancements

- Multi-hand gesture support
- User-specific calibration
- Cross-platform audio abstraction
- Push-to-talk gesture
- Desktop (.exe) deployment

---

## 14. Evaluation Criteria Mapping

| Milestone | Evaluation Focus |
|---------|------------------|
| Week 2 | Real-time webcam & landmark detection |
| Week 4 | Accurate gesture classification |
| Week 6 | Smooth volume control |
| Week 8 | Stable UI & user experience |

---

## 15. Conclusion

This project demonstrates a complete **engineering pipeline** from vision-based sensing to OS-level control with real-time feedback. The use of normalized gesture logic, modular architecture, and system APIs elevates it beyond a prototype into a production-grade academic system.

---

## 16. Academic Relevance

Covers concepts from:
- Computer Vision
- Human–Computer Interaction
- Operating Systems
- Software Architecture
- Real-Time Systems

Suitable for **mini-projects, major projects, and technical evaluations**.

