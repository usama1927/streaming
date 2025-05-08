from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.models import video
from app.utils.blob import upload_to_blob
from app.models import db, video as video_model


from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter()

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@router.post("/upload")
async def upload_video(
    title: str = Form(...),
    caption: str = Form(""),
    location: str = Form(""),
    people: str = Form(""),
    video_file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("Received upload:")
    print(f"title={title}, file={video_file.filename if video_file else 'None'}")
    if user["role"] != "creator":
        return {"error": "Only creators can upload videos"}

    blob_url = upload_to_blob(video_file.file, video_file.filename)

    new_video = video_model.Video(
        title=title,
        url=blob_url,
        caption=caption,
        location=location,
        people=people,
        owner_id=user["id"]
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return {
        "message": "Video uploaded successfully",
        "video_url": blob_url,
        "video_id": new_video.id
    }


@router.get("/my-uploads")
def list_my_uploads(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "creator":
        return {"error": "Unauthorized"}

    videos = db.query(video.Video).filter(video.Video.owner_id == user["id"]).all()
    return [
        {
            "id": v.id,
            "title": v.title,
            "url": v.url,
            "caption": v.caption,
            "location": v.location,
            "people": v.people
        }
        for v in videos
    ]



