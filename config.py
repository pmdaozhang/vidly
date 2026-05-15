import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://www.googleapis.com/youtube/v3"
MAX_RESULTS = 20
