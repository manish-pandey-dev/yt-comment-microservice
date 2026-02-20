from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True)
    title = Column(String)
    published_at = Column(DateTime)
    transcript = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
