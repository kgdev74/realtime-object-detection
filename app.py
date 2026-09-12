"""
Local development entrypoint.
Runs the Flask application locally on http://127.0.0.1:5000
"""
from api.index import app

if __name__ == "__main__":
    print("[INFO] Starting Object Detection Web App on http://127.0.0.1:5000")
    print("[INFO] Ready for local use and Vercel deployment.")
    app.run(host="0.0.0.0", port=5000, debug=True)
