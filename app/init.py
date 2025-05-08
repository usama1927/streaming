# app/models/init.py or db.py if you prefer
from app.models.db import Base, engine, SessionLocal

def init_db():
    # 🔁 Local import avoids circular dependencies
    from app.models import user, video, comment, rating

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Seed data
    session = SessionLocal()
    try:
        if not session.query(user.User).filter_by(username="creator1").first():
            session.add(user.User(username="creator1", password="creatorpass", role="creator"))
        if not session.query(user.User).filter_by(username="creator2").first():
            session.add(user.User(username="creator2", password="creatorpass", role="creator"))
        session.commit()
    finally:
        session.close()
