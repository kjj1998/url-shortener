"""Main FastAPI application."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from url_shortener.web.api.api import router as url_shortener_router

app = FastAPI(
    docs_url="/url-shortener/docs",
    redoc_url=None,
    openapi_url="/url-shortener/openapi.json",
)

origins = ["http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    url_shortener_router, prefix="/url-shortener", tags=["url_shortener"]
)


@app.get("/url-shortener")
async def root():
    """Root endpoint."""
    return {"message": f"Hello from {os.getenv("HOSTNAME", default="local")}"}
