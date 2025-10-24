# app.py
from flask import Flask, request, redirect
import csv
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = "clicks.csv"
REDIRECT_URL = "https://example.com"  # where to send teachers after click

# --- ensure CSV file exists ---
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "timestamp", "ip", "user_agent"])


@app.route("/<teacher_email>")
def track_click(teacher_email):
    # record the click
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([teacher_email, timestamp, ip, user_agent])

    # redirect to your main page or thank-you page
    return redirect(REDIRECT_URL)


@app.route("/")
def home():
    return "<h3>Teacher Click Tracker is Running ✅</h3>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
