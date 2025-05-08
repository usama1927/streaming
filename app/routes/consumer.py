from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.models import db, video, comment, rating
from app.auth.auth import get_current_user

router = APIRouter()

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.get("/videos")
def get_all_videos(db: Session = Depends(get_db)):
    videos = db.query(video.Video).all()
    return [
        {
            "id": v.id,
            "title": v.title,
            "caption": v.caption,
            "location": v.location,
            "people": v.people,
            "url": v.url,
            "ratings": [r.value for r in v.ratings],
            "comments": [c.text for c in v.comments]
        }
        for v in videos
    ]

@router.post("/comment")
def post_comment(
    video_id: int = Form(...),
    text: str = Form(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user["role"] != "consumer":
        return {"error": "Only consumers can comment"}

    new_comment = comment.Comment(
        video_id=video_id,
        user_id=user["id"],
        text=text
    )
    db.add(new_comment)
    db.commit()
    return {"message": "Comment added"}

@router.post("/rate")
def rate_video(
    video_id: int = Form(...),
    rating_value: int = Form(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user["role"] != "consumer":
        return {"error": "Only consumers can rate"}

    new_rating = rating.Rating(
        video_id=video_id,
        user_id=user["id"],
        value=rating_value
    )
    db.add(new_rating)
    db.commit()
    return {"message": "Rating submitted"}


