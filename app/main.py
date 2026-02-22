from fastapi import FastAPI
from datetime import datetime
from app.db.database import Base, engine
from app.db.database import SessionLocal
from app.db.models import Video
from app.db.models import Comment
from app.services.youtube_service import fetch_latest_video
from app.services.transcript_service import fetch_transcript
from app.services.ai_service import summarize_transcript, generate_comment


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

    transcript = fetch_transcript(latest["video_id"])

    summary = None
    generated = None

    if transcript:
        summary = summarize_transcript(transcript)
        generated = generate_comment(summary)

    video = Video(
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
