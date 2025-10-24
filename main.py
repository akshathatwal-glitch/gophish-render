from flask import Flask, request, Response
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# --- load .env variables ---
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# --- your 404 HTML page ---
ERROR_404_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>404 Not Found</title>
    <style>
        body {
            background-color: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
            color: #222;
        }
        h1 {
            font-size: 80px;
            font-weight: bold;
            margin: 0;
        }
        p {
            font-size: 24px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>ERROR 404</h1>
    <p>website not available</p>
</body>
</html>
"""

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

    # return custom 404 page instead of redirect
    return Response(ERROR_404_HTML, status=404, mimetype="text/html")

@app.route("/")
def home():
    return Response(ERROR_404_HTML, status=404, mimetype="text/html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
