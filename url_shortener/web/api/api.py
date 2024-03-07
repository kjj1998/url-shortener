"""APIs for the URL shortener app."""

from fastapi import APIRouter
from .schemas import UrlShortenRequest
from ...shortener_service.shortener_service import UrlShortenerService

router = APIRouter()


@router.get("/{short_url}")
def redirect_to_long_url(short_url: str):
    """Redirect to the original URL."""
    print(short_url)


@router.post("/")
def shorten_url(long_url: UrlShortenRequest):
    """Shorten the given URL."""
    url_shortener_service: UrlShortenerService = UrlShortenerService()
    return url_shortener_service.shorten_url(long_url.url)
