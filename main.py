import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from crud import create_db_url, get_db_url_by_key
from db import SessionLocal, engine
from models import Base
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
async def create_url(url: URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="Your provided URL is not valid")

    db_url = create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key
    return db_url


@app.get("/{url_key}")
async def fw(url_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = get_db_url_by_key(db=db, url_key=url_key)
    if db_url:
        return RedirectResponse(db_url.target_url)
    else:
        raise HTTPException(status_code=404, detail=f"{url_key} doesn't exist")
