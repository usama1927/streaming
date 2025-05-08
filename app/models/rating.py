from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.db import Base


class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = {'schema': 'public'}  # ✅ Force table to public schema
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer)  # 1–5 scale
    video_id = Column(Integer, ForeignKey("public.videos.id"))
    user_id = Column(Integer, ForeignKey("public.users.id"))

    video = relationship("Video", back_populates="ratings")
