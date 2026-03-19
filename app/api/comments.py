from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Comment
from app.services.youtube_post_service import post_comment

router = APIRouter(prefix="/comments", tags=["Comments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/pending")
def get_pending_comments(db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.status == "pending").all()
    return comments


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

    # Call YouTube API
    post_comment(comment.video_id, comment.content)

    comment.status = "posted"
    db.commit()

    return {"message": "Comment posted successfully"}
