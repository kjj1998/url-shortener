"""Schemas for the API."""

from datetime import datetime

from pydantic import BaseModel, AnyUrl

class UrlShortenRequest(BaseModel):
    """Schema for the request to shorten a URL."""
    url: AnyUrl

class GetShortenedUrlSchema(BaseModel):
    """Shortene URL schema."""
    id: str
    long_url: str
    short_url: str
    created: datetime
