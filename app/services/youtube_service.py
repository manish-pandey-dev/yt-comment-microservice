import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

def fetch_latest_video(channel_id: str):
    params = {
        "key": API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": 1,
        "type": "video"
    }

    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    response.raise_for_status()

    data = response.json()
    item = data["items"][0]

    return {
        "video_id": item["id"]["videoId"],
        "title": item["snippet"]["title"],
        "published_at": item["snippet"]["publishedAt"]
    }
