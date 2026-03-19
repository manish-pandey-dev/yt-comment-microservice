import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from app.db.database import SessionLocal
from app.db.models import OAuthToken
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def post_comment(video_id: str, comment_text: str):
    db = SessionLocal()
    token_row = db.query(OAuthToken).first()
    db.close()

    if not token_row:
        raise Exception("No OAuth token found")

    credentials = Credentials(
        token=None,
        refresh_token=token_row.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        scopes=SCOPES,
    )

    # Force refresh access token
    credentials.refresh(Request())

    youtube = build("youtube", "v3", credentials=credentials)

    request = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
    )

    return request.execute()
