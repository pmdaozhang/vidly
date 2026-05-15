from flask import Flask, render_template, request, jsonify
from youtube_api import search_videos, check_api_key
from config import YOUTUBE_API_KEY

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json()
    keywords = data.get("keywords", "").split(",")
    keywords = [kw.strip() for kw in keywords if kw.strip()]
    time_range = data.get("time_range", "")
    max_results = int(data.get("max_results", 10))
    language = data.get("language", "zh")
    duration = data.get("duration", "all")

    if not keywords:
        return jsonify({"error": "Please enter at least one keyword"}), 400

    results = {}
    for kw in keywords:
        results[kw] = search_videos(kw, time_range, max_results, language, duration)
    return jsonify(results)


@app.route("/api/check-key")
def api_check_key():
    valid = check_api_key()
    return jsonify({"valid": valid})


if __name__ == "__main__":
    if YOUTUBE_API_KEY == "YOUR_API_KEY_HERE":
        print("WARNING: YOUTUBE_API_KEY is not configured. Please set it in .env")
    app.run(host="0.0.0.0", port=5000, debug=True)
