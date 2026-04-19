from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.database import SessionLocal
from app.db.models import Channel
import os
import requests

router = APIRouter(prefix="/channels", tags=["Channels"])


# ---------------------------------------------------------------------------
# Request body: what caller must send when adding a channel
# ---------------------------------------------------------------------------
class ChannelCreateRequest(BaseModel):
    name: str        # Human label e.g. "Tech With Tim"
    channel_id: str  # YouTube channel ID e.g. "UCVhQ2NnY5Rskt6UjCUkJ_DA"


# ---------------------------------------------------------------------------
# GET /channels/ — list all registered channels
# ---------------------------------------------------------------------------
@router.get("/")
def list_channels():
    db = SessionLocal()
    try:
        channels = db.query(Channel).order_by(Channel.created_at.desc()).all()
        return channels
    finally:
        db.close()


# ---------------------------------------------------------------------------
# POST /channels/ — register a new channel
# ---------------------------------------------------------------------------
@router.post("/")
def add_channel(payload: ChannelCreateRequest):
    db = SessionLocal()
    try:
        # Guard: no duplicate YouTube channel IDs
        existing = db.query(Channel).filter(
            Channel.channel_id == payload.channel_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Channel '{payload.channel_id}' is already registered"
            )

        channel = Channel(
            name=payload.name,
            channel_id=payload.channel_id
        )

        db.add(channel)
        db.commit()
        db.refresh(channel)

        return {
            "message": "Channel added successfully",
            "channel": {
                "id": channel.id,
                "name": channel.name,
                "channel_id": channel.channel_id,
                "created_at": channel.created_at
            }
        }
    finally:
        db.close()


# ---------------------------------------------------------------------------
# GET /channels/resolve?url= — extract channel ID from any YouTube video URL
# User pastes a video URL, we return the channel ID + name automatically
# ---------------------------------------------------------------------------
@router.get("/resolve")
def resolve_channel(url: str):
    api_key = os.getenv("YOUTUBE_API_KEY")

    # Extract video ID from URL
    # Supports: youtube.com/watch?v=XXX and youtu.be/XXX
    video_id = None

    if "watch?v=" in url:
        video_id = url.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]

    if not video_id:
        raise HTTPException(
            status_code=400,
            detail="Could not extract video ID from URL. Use youtube.com/watch?v=... or youtu.be/..."
        )

    # Call YouTube API to get channel info from video
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/videos",
        params={
            "key": api_key,
            "id": video_id,
            "part": "snippet"
        }
    )

    data = response.json()

    if not data.get("items"):
        raise HTTPException(
            status_code=404,
            detail="Video not found. Check the URL and try again."
        )

    snippet = data["items"][0]["snippet"]

    return {
        "channel_id": snippet["channelId"],
        "channel_name": snippet["channelTitle"],
        "video_title": snippet["title"]
    }


# ---------------------------------------------------------------------------
# DELETE /channels/{id} — remove a channel by internal integer ID
# ---------------------------------------------------------------------------
@router.delete("/{channel_id}")
def delete_channel(channel_id: int):
    db = SessionLocal()
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()

        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")

        db.delete(channel)
        db.commit()

        return {"message": f"Channel '{channel.name}' removed successfully"}
    finally:
        db.close()