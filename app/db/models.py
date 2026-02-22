from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True)
    title = Column(String)
    published_at = Column(DateTime)
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, ForeignKey("videos.video_id"))
    content = Column(Text)
    status = Column(String, default="pending")  # pending/approved/posted/rejected
    created_at = Column(DateTime, default=datetime.utcnow)
