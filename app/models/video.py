from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.db import Base

class Video(Base):
    __tablename__ = "videos"
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    caption = Column(String)
    location = Column(String)
    people = Column(String)
    owner_id = Column(Integer, ForeignKey("public.users.id"))  # ✅ Fix here

    comments = relationship("Comment", back_populates="video")
    ratings = relationship("Rating", back_populates="video")
