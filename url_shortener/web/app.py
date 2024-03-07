"""Main FastAPI application."""

from fastapi import FastAPI
from url_shortener.web.api.api import router as url_shortener_router

app = FastAPI()

app.include_router(url_shortener_router, tags=["url_shortener"])
