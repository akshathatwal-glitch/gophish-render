from flask import Flask, request, redirect
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# --- load .env variables ---
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
REDIRECT_URL = os.getenv("REDIRECT_URL", "https://example.com")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route("/<teacher_email>")
def track_click(teacher_email):
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")

    # store click in Supabase
    supabase.table("clicks").insert({
        "email": teacher_email,
        "ip": ip,
        "user_agent": user_agent
    }).execute()

    return redirect(REDIRECT_URL)

@app.route("/")
def home():
    return "<h3>Teacher Click Tracker with Supabase ✅</h3>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
