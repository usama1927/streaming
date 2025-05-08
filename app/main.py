from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import creator, consumer
from app.auth.auth import auth_router
from app.init import init_db
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.routes.creator import get_db



app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init PostgreSQL tables
init_db()

# Include API routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(creator.router, prefix="/creator", tags=["creator"])
app.include_router(consumer.router, prefix="/consumer", tags=["consumer"])

# Serve static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Frontend routes
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/video/{video_id}")
def video_detail(video_id: int, request: Request, db: Session = Depends(get_db)):
    from app.models.video import Video
    from app.models.comment import Comment
    from app.models.rating import Rating

    v = db.query(Video).filter_by(id=video_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Video not found")

    avg_rating = round(sum(r.value for r in v.ratings) / len(v.ratings), 1) if v.ratings else "N/A"
    return templates.TemplateResponse("video_detail.html", {
        "request": request,
        "video": v,
        "avg_rating": avg_rating,
        "comments": v.comments
    })
