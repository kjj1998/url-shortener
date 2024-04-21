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
    username: str | None

class Token(BaseModel):
    """Schema for the JWT token response"""

    access_token: str
    token_type: str