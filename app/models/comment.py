from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.db import Base

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {'schema': 'public'}  # ✅ Force table to public schema
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    video_id = Column(Integer, ForeignKey("public.videos.id"))
    user_id = Column(Integer, ForeignKey("public.users.id"))

    video = relationship("Video", back_populates="comments")
