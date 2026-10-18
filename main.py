import secrets
import string

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db import SessionLocal, engine
from models import URL, Base
from schemas import URLBase, URLInfoResponse

app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return "Welcome to my URL shortener API"


@app.post("/url", response_model=URLInfoResponse)
def create_url(url: URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="Your provided URL is not valid")

    chars = string.ascii_uppercase
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = URL(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url


@app.get("/{url_key}")
def fw(url_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.key == url_key, URL.is_active).first()
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise HTTPException(status_code=404, detail=f"{url_key} doesn't exist")
