import os
from flask import Flask, render_template, jsonify

# Locate the root templates directory regardless of whether
# the app is run locally or on Vercel Serverless environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)


@app.route("/")
def index():
    """Renders the real-time object detection web dashboard."""
    return render_template("index.html")


@app.route("/api/health")
def health():
    """Health check endpoint for Vercel monitoring."""
    return jsonify({
        "status": "online",
        "engine": "COCO-SSD / WebGL",
        "platform": "Vercel Serverless Python"
    })


# For local testing via 'python api/index.py'
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
