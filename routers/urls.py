from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import URL
from schemas import URLCreate, URLResponse
from datetime import datetime, timezone
from fastapi.responses import FileResponse
import random
import string
import os

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

router = APIRouter()

def generate_short_code():
    return "".join(random.choices(string.ascii_letters+ string.digits,k=6))

@router.get("/")
def home():
    return FileResponse("static/index.html")

@router.post("/shorten", response_model=URLResponse)
def create_short_url(data: URLCreate, db: Session = Depends(get_db)):
    
    if data.custom_code :
        existing = db.query(URL).filter(URL.short_code == data.custom_code).first()
        if existing :
            raise HTTPException(status_code=409, detail = "Custom code already in use")
        short_code = data.custom_code
    else :
      while True:
          short_code = generate_short_code()
          if db.query(URL).filter(URL.short_code == short_code).first() is None:
              break

    combined_url = BASE_URL + "/" + short_code
    final_url = URL(short_code=short_code, original_url=str(data.url), expires_at = data.expires_at)
    db.add(final_url)
    db.commit()

    return URLResponse(short_url=combined_url)

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    local_url = db.query(URL).filter(URL.short_code == short_code).first()

    if local_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    if local_url.expires_at and local_url.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="This link has expired")
    
    local_url.clicks+=1
    db.commit()
    return RedirectResponse(local_url.original_url)

@router.get("/{short_code}/stats")
def get_stats(short_code:str, db : Session = Depends(get_db)):
    local_url = db.query(URL).filter(URL.short_code == short_code).first()

    if local_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    return{
        "short_code":short_code,
        "original_url":local_url.original_url,
        "clicks":local_url.clicks,
        "created_at":local_url.created_at,
        "expires_at":local_url.expires_at
    }