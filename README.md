# 🎯 Real-Time Object Detection Web App (Vercel Edition)

A high-performance real-time object detection web application built with **Flask (Python)**, **TensorFlow.js (COCO-SSD)**, and **HTML5 Canvas**, fully optimized for deployment on **Vercel Serverless**.

Detects 80 common object classes (person, cell phone, laptop, bottle, cup, chair, dog, etc.) in real-time at 30–60 FPS directly in the user's browser with zero server latency.

---

## ⚡ Why This Architecture is Vercel-Ready

Traditional OpenCV (`cv2.VideoCapture(0)`) and PyTorch setups cannot deploy to Vercel because:
1. **Cloud Serverless containers have no physical webcam attached.**
2. **PyTorch + OpenCV exceeds 1.5 GB**, vastly exceeding Vercel's 250 MB serverless function limit.
3. **Infinite streaming loops time out** on serverless infrastructure.

**Our Vercel Solution:**
- **Browser-Powered Vision**: Accesses the user's real camera securely via `navigator.mediaDevices.getUserMedia()` and executes computer vision models utilizing WebGL GPU hardware acceleration.
- **Lightweight Serverless Python Backend**: Standard Vercel Serverless Function structure (`api/index.py` + `vercel.json`), deploying in seconds with minimal package overhead.

---

## 🚀 How to Deploy on Vercel (Recommended: 1-Click via GitHub)

### Method 1: Deploy via Vercel Dashboard (Easiest)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Update for Vercel deployment"
   git push -u origin main
   ```

2. **Go to Vercel**:
   - Open [vercel.com](https://vercel.com) and log in (e.g. with your GitHub account).
   - Click **"Add New..."** > **"Project"**.
   - Import your repository: `kgdev74/realtime-object-detection`.

3. **Deploy**:
   - Leave the default settings as they are (Vercel automatically detects `vercel.json` and `api/index.py`).
   - Click **Deploy**.
   - In less than 30 seconds, your site will be live at `https://your-project.vercel.app`! 🎉

---

### Method 2: Deploy via Vercel CLI

If you have Node.js and npm installed:

```bash
# 1. Install the Vercel CLI globally
npm install -g vercel

# 2. Login to your Vercel account
vercel login

# 3. Deploy to production
vercel --prod
```

---

## 💻 Local Development

### 1. Set Up Virtual Environment

```bash
# Windows
py -3.13 -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Locally

```bash
python app.py
```

Open your browser at **`http://127.0.0.1:5000`** and allow camera permissions when prompted.

---

## 📁 Project Structure

```
obj_detector/
│
├── api/
│   └── index.py           # Vercel Serverless Python entrypoint (Flask)
├── templates/
│   └── index.html         # Modern web interface with real-time WebGL detection
├── vercel.json            # Vercel routing and runtime configuration
├── app.py                 # Local development entrypoint
├── requirements.txt       # Lightweight dependencies (< 50MB)
└── README.md              # Documentation and deployment guide
```

---

## 🏷️ Detected Object Categories (80 Classes)

The model recognizes 80 common categories from the Microsoft COCO dataset:
- **People & Accessories**: `person`, `backpack`, `umbrella`, `handbag`, `tie`, `suitcase`
- **Electronics**: `cell phone`, `laptop`, `mouse`, `remote`, `keyboard`, `tv`, `microwave`, `oven`, `toaster`, `clock`
- **Vehicles**: `car`, `motorcycle`, `airplane`, `bus`, `train`, `truck`, `boat`, `bicycle`
- **Household & Kitchen**: `bottle`, `wine glass`, `cup`, `fork`, `knife`, `spoon`, `bowl`, `chair`, `couch`, `potted plant`, `bed`, `dining table`, `sink`, `refrigerator`, `book`, `vase`, `scissors`
- **Animals**: `bird`, `cat`, `dog`, `horse`, `sheep`, `cow`, `elephant`, `bear`, `zebra`, `giraffe`
- **Food**: `banana`, `apple`, `sandwich`, `orange`, `broccoli`, `carrot`, `hot dog`, `pizza`, `donut`, `cake`
- **Sports**: `frisbee`, `skis`, `snowboard`, `sports ball`, `kite`, `baseball bat`, `baseball glove`, `skateboard`, `surfboard`, `tennis racket`
