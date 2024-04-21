"""Schemas for the API."""

from datetime import datetime

from pydantic import BaseModel, AnyUrl

class UrlShortenRequest(BaseModel):
    """Schema for the request to shorten a URL."""

    url: AnyUrl

class Url(BaseModel):
    """Shortened URL schema."""

    id: str
    username: str | None

class GetUrl(Url):
    """Shortened URL schema."""

    long_url: str
    short_url: str
    created: datetime

class Token(BaseModel):
    """Schema for the JWT token response"""

    access_token: str
    token_type: str
