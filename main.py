import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL as StarletteURL

from config import get_settings
from crud import (
    create_db_url,
    deactivate_db_url_by_secret_key,
    get_db_url_by_key,
    get_db_url_by_secret_key,
    update_db_clicks,
)
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


def get_admin_info(db_url: URL) -> URLInfoResponse:
    base_url = StarletteURL(get_settings().base_url)
    admin_endpoint = app.url_path_for("admin info", secret_key=db_url.secret_key)
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@app.post("/url", response_model=URLInfoResponse)
async def create_url(url: URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="Your provided URL is not valid")

    db_url = create_db_url(db=db, url=url)
    return get_admin_info(db_url)


@app.get("/{url_key}")
async def fw(url_key: str, request: Request, db: Session = Depends(get_db)):
    db_url = get_db_url_by_key(db=db, url_key=url_key)
    if db_url:
        update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise HTTPException(status_code=404, detail=f"{url_key} doesn't exist")


@app.get("/admin/{secret_key}", name="admin info", response_model=URLInfoResponse)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := get_db_url_by_secret_key(db, secret_key=secret_key):
        return get_admin_info(db_url)
    else:
        raise HTTPException(status_code=404, detail=f"{secret_key} doesn't exist")


@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := deactivate_db_url_by_secret_key(db, secret_key=secret_key):
        msg = f"Successfully deleted shortened URL {db_url.target_url}"
        return {"detail": msg}
    else:
        raise HTTPException(status_code=404, detail=f"{secret_key} doesn't exist")
