from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models import db, user
from app.utils.jwt import create_access_token
from jose import JWTError, jwt
import os

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@auth_router.post("/register")
def register(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Register only consumer accounts
    db_user = db.query(user.User).filter(user.User.username == form.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = user.User(username=form.username, password=form.password, role="consumer")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Registered as consumer"}

@auth_router.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(user.User).filter(user.User.username == form.username).first()
    if not db_user or db_user.password != form.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY", "mysecret"), algorithms=["HS256"])
        username = payload.get("sub")
        role = payload.get("role")
        db_user = db.query(user.User).filter(user.User.username == username).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"username": username, "role": role, "id": db_user.id}
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
