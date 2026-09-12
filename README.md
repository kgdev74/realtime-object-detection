# Real-Time Object Detection Web App

A clean, beginner-friendly web application for real-time object detection using **Python**, **OpenCV**, **Flask**, and **Ultralytics YOLOv8**.

The app captures video from your webcam, detects common objects (person, phone, cup, laptop, bottle, etc.) with bounding boxes and confidence scores, and streams the annotated video directly to a modern web dashboard using standard MJPEG HTTP streaming.

---

## 📁 Project Structure

```
obj_detector/
│
├── app.py                 # Flask app, OpenCV capture, YOLOv8 inference, MJPEG generator
├── requirements.txt       # Minimal package dependencies
├── templates/
│   └── index.html         # Modern web interface displaying the live feed
└── README.md              # Step-by-step setup and usage instructions
```

---

## 🚀 Quickstart Guide

### Prerequisites

- **Python 3.10 - 3.13** installed on your system.
- A built-in or USB webcam connected.

---

### Step 1: Clone or Navigate to the Project Directory

Open your terminal (PowerShell or Command Prompt on Windows, or Bash on macOS/Linux) and navigate to the project folder:

```bash
cd path/to/obj_detector
```

---

### Step 2: Create a Virtual Environment

Isolating dependencies ensures a clean, reproducible setup.

#### On Windows (PowerShell):

```powershell
py -3.13 -m venv .venv
# or: python -m venv .venv
```

#### On macOS / Linux:

```bash
python3 -m venv .venv
```

---

### Step 3: Activate the Virtual Environment

#### On Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

_(If you see an execution policy error on PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and retry)._

#### On Windows (Command Prompt `cmd`):

```cmd
.venv\Scripts\activate.bat
```

#### On macOS / Linux:

```bash
source .venv/bin/activate
```

---

### Step 4: Install Dependencies

Install Flask, OpenCV, and Ultralytics YOLOv8:

```bash
pip install -r requirements.txt
```

---

### Step 5: Run the Application

Start the Flask server:

```bash
python app.py
```

> **Note**: On the first run, Ultralytics will automatically download the lightweight `yolov8n.pt` model weights (~6 MB).

---

### Step 6: View the Live Detection Stream

Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

or

```
http://localhost:5000
```

Hold everyday items in front of your camera (like your phone, bottle, backpack, or keys) to see bounding boxes, labels, and detection confidence in real time!

To stop the server and release camera resources cleanly, press `Ctrl + C` in your terminal.

---

## 🧠 How It Works (For Beginners)

1. **Webcam Capture (`cv2.VideoCapture(0)`)**:
   OpenCV connects to camera device index `0`. Inside `generate_frames()`, `camera.read()` continuously grabs the newest video frame as a NumPy array of pixels.
2. **YOLOv8 Inference (`model(frame)`)**:
   Each image is fed into the YOLOv8 Nano deep learning model. The model identifies objects in milliseconds. `results[0].plot()` draws colored bounding boxes, class names, and confidence percentages.
3. **MJPEG HTTP Streaming (`multipart/x-mixed-replace`)**:
   Instead of complex WebSockets or WebRTC setups, OpenCV encodes each processed frame into a JPEG buffer (`cv2.imencode`). Flask yields these byte buffers wrapped in the standard MJPEG multipart boundary. The browser's standard HTML `<img>` tag natively displays this continuous stream seamlessly.
4. **Resource Management**:
   Whenever a client disconnects or the Flask app shuts down, `camera.release()` ensures your webcam is freed and the hardware lock is released.

---

## 🛠️ Troubleshooting

- **Camera Not Found / Blank Frame**:
  - Check camera permissions in **Windows Settings > Privacy & Security > Camera** and ensure desktop apps have access.
  - If you have multiple cameras (or virtual cameras like OBS), you can change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` in `app.py`.
- **Port 5000 in Use**:
  - In `app.py`, change `app.run(port=5000)` to `app.run(port=5001)`.
