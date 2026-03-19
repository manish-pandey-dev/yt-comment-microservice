from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.oauth_service import create_oauth_flow
from google.oauth2.credentials import Credentials
import os
from app.db.database import SessionLocal
from app.db.models import OAuthToken

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth_state = {}

@router.get("/login")
def login():
    flow = create_oauth_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    oauth_state["state"] = state
    return RedirectResponse(auth_url)

@router.get("/callback")
def callback(state: str, code: str):
    flow = create_oauth_flow()
    flow.fetch_token(code=code)

    credentials = flow.credentials
    
    refresh_token = credentials.refresh_token
    print("REFRESH TOKEN:", refresh_token)

    db = SessionLocal()

    # Remove old token if exists
    db.query(OAuthToken).delete()

    token = OAuthToken(
        refresh_token=credentials.refresh_token
    )

    db.add(token)
    db.commit()
    db.close()

    return {"message": "Authentication successful and token stored"}
