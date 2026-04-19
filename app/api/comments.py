from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Comment
from app.services.youtube_post_service import post_comment
from typing import Optional

router = APIRouter(prefix="/comments", tags=["Comments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# GET /comments/pending — now supports optional status and channel filter
# ---------------------------------------------------------------------------
@router.get("/pending")
def get_comments(
        status: Optional[str] = Query(None),
        channel_id: Optional[str] = Query(None),
        db: Session = Depends(get_db)
):
    query = db.query(Comment)

    # Filter by status if provided, otherwise return all
    if status:
        query = query.filter(Comment.status == status)

    # Filter by channel if provided
    if channel_id:
        query = query.filter(Comment.channel_id == channel_id)

    return query.order_by(Comment.created_at.desc()).all()


@router.post("/{comment_id}/approve")
def approve_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.status != "pending":
        raise HTTPException(status_code=400, detail="Comment is not pending")
    comment.status = "approved"
    db.commit()
    return {"message": "Comment approved", "id": comment_id}


@router.post("/{comment_id}/reject")
def reject_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment.status = "rejected"
    db.commit()
    return {"message": "Comment rejected", "id": comment_id}


@router.post("/{comment_id}/post")
def post_approved_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.status != "approved":
        raise HTTPException(status_code=400, detail="Comment must be approved first")
    post_comment(comment.video_id, comment.content)
    comment.status = "posted"
    db.commit()
    return {"message": "Comment posted successfully"}