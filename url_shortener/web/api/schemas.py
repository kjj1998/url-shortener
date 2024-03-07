"""Schemas for the API."""

from pydantic import BaseModel, AnyUrl

class UrlShortenRequest(BaseModel):
    """Schema for the request to shorten a URL."""
    url: AnyUrl