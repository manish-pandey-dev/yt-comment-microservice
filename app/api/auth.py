from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services.oauth_service import create_oauth_flow
from app.db.database import SessionLocal
from app.db.models import OAuthToken
import hashlib, base64, secrets

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth_state = {}

@router.get("/login")
def login():
    flow = create_oauth_flow()
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b"=").decode()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
        code_challenge=code_challenge,
        code_challenge_method="S256"
    )
    oauth_state["state"] = state
    oauth_state["code_verifier"] = code_verifier
    return RedirectResponse(auth_url)


@router.get("/callback")
def callback(state: str, code: str):
    flow = create_oauth_flow()
    flow.fetch_token(
        code=code,
        code_verifier=oauth_state.get("code_verifier")
    )
    credentials = flow.credentials
    print("REFRESH TOKEN:", credentials.refresh_token)
    db = SessionLocal()
    db.query(OAuthToken).delete()
    db.add(OAuthToken(refresh_token=credentials.refresh_token))
    db.commit()
    db.close()
    return {"message": "Authentication successful and token stored"}