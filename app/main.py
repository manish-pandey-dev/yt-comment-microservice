from fastapi import FastAPI
from app.db.database import Base, engine
from app.services.youtube_service import fetch_latest_video
from app.db.database import SessionLocal
from app.db.models import Video
from datetime import datetime

app = FastAPI(title="YT Comment Microservice")

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/check")
def check_latest_video():
    db = SessionLocal()

    latest = fetch_latest_video()

    existing = db.query(Video).filter_by(video_id=latest["video_id"]).first()

    if existing:
        return {"message": "No new video"}

    video = Video(
        video_id=latest["video_id"],
        title=latest["title"],
        published_at=datetime.fromisoformat(latest["published_at"].replace("Z", "+00:00"))
    )

    db.add(video)
    db.commit()

    return {"message": "New video stored", "video": latest}
