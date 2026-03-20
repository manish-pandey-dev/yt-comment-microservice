from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from datetime import datetime
from app.db.database import Base, engine
from app.db.database import SessionLocal
from app.db.models import Video
from app.db.models import Comment
from app.db.models import Channel
from app.services.youtube_service import fetch_latest_video
from app.services.transcript_service import fetch_transcript
from app.services.ai_service import summarize_transcript, generate_comment
from app.api.comments import router as comments_router
from app.api.auth import router as auth_router

app = FastAPI(title="YT Comment Microservice")
app.include_router(comments_router)
app.include_router(auth_router)

templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/channels")
def get_channels():
    db = SessionLocal()
    channels = db.query(Channel).all()
    return channels

@app.get("/check/{channel_id}")
def check_latest_video(channel_id: int):
    db = SessionLocal()
    
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        return {"error": "Channel not found"}

    latest = fetch_latest_video(channel.channel_id)

    existing = db.query(Video).filter_by(video_id=latest["video_id"],channel_id=channel.id).first()

    if existing:
        return {"message": "No new video"}

    transcript = fetch_transcript(latest["video_id"])

    summary = None
    generated = None

    if transcript:
        summary = summarize_transcript(transcript)
        generated = generate_comment(summary)

    video = Video(
        channel_id=channel.channel_id,
        video_id=latest["video_id"],
        title=latest["title"],
        published_at=datetime.fromisoformat(
            latest["published_at"].replace("Z", "+00:00")
        ),
        transcript=transcript,
        summary=summary
    )

    db.add(video)
    db.commit()

    if generated:
        comment = Comment(
            channel_id=channel.channel_id,
            video_id=latest["video_id"],
            content=generated,
            status="pending"
        )

        db.add(comment)
        db.commit()



    return {
        "message": "New video stored",
        "video": latest,
        "comment_generated": generated
    }
