"""
Real-Time Object Detection Web Application
------------------------------------------
Tech Stack:
- Python 3
- Flask (Web framework & MJPEG streaming)
- OpenCV (cv2: Video capture and image encoding)
- Ultralytics YOLOv8 (Pre-trained yolov8n.pt deep learning model)

How It Works:
1. WEBCAM CAPTURE: OpenCV connects to your system's default camera (cv2.VideoCapture(0))
   and reads incoming video frames one-by-one in an infinite loop.
2. MODEL INFERENCE: Each raw frame (numpy array) is passed into the lightweight YOLOv8 Nano
   model. The model identifies objects, predicts bounding box coordinates, class labels,
   and confidence scores. Using results[0].plot(), OpenCV renders these annotations directly
   onto the frame.
3. MJPEG HTTP STREAMING: Each annotated frame is encoded into a JPEG byte sequence and yielded
   as a multipart chunk (Content-Type: multipart/x-mixed-replace). The browser's <img> tag
   continuously receives and replaces each image chunk, creating a smooth live video stream.
4. RESOURCE CLEANUP: When the browser disconnects or the server stops, camera resources
   are safely released with cap.release().
"""

import time
import atexit
import cv2
from flask import Flask, render_template, Response
from ultralytics import YOLO

# 1. Initialize Flask Application and Load YOLOv8 Model
app = Flask(__name__)


print("[INFO] Loading YOLOv8n model...")
model = YOLO("yolov8n.pt")
print("[INFO] Model loaded successfully.")

active_camera = None


def get_camera():
    """
    Initializes and returns a cv2.VideoCapture object for the default webcam.
    cv2.VideoCapture(0) accesses index 0 (the primary built-in or USB webcam).
    """
    global active_camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    active_camera = cap
    return cap


def create_standby_frame(message="Webcam not detected"):
    """
    Generates a synthetic diagnostic frame if the webcam is missing or busy.
    Prevents the server from crashing and displays helpful status on the webpage.
    """
    import numpy as np

    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Dark background with alert box
    cv2.rectangle(frame, (40, 180), (600, 300), (30, 30, 30), -1)
    cv2.rectangle(frame, (40, 180), (600, 300), (0, 140, 255), 2)
    cv2.putText(
        frame,
        message,
        (60, 230),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        "Check permissions or connect a camera.",
        (60, 270),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (180, 180, 180),
        1,
        cv2.LINE_AA,
    )
    ret, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes()

# 2. Frame Generator (Inference Loop & MJPEG Packaging)
def generate_frames():
    """
    Continuous generator that captures frames from the webcam, runs YOLOv8
    object detection, draws bounding boxes and labels, and formats the output
    as an MJPEG stream for the web browser.
    """
    camera = get_camera()

    try:
        while True:
           
            success, frame = camera.read()

            if not success:
                
                frame_bytes = create_standby_frame("Webcam unavailable / No input")
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )
                time.sleep(1.0)
                continue

            
            results = model(frame, verbose=False)

            
            annotated_frame = results[0].plot()
            ret, buffer = cv2.imencode(".jpg", annotated_frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

    finally:
        print("[INFO] Releasing webcam resources...")
        camera.release()

# 3. Web Routes
@app.route("/")
def index():
    """
    Renders the main dashboard interface.
    """
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    """
    Video streaming route. The response yields MJPEG frames continuously
    using the multipart/x-mixed-replace content type.
    """
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

# 4. Graceful Application Teardown
def cleanup():
    """Ensures camera is safely released if the application exits."""
    global active_camera
    if active_camera is not None and active_camera.isOpened():
        print("[INFO] Closing camera on application exit...")
        active_camera.release()


atexit.register(cleanup)

# 5. Application Entry Point
if __name__ == "__main__":
    print("[INFO] Starting Flask server on http://127.0.0.1:5000")
    print("[INFO] Press Ctrl+C to terminate.")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)

