"""APIs for the URL shortener app."""

from fastapi import APIRouter

from url_shortener.repository.unit_of_work import UnitOfWork
from url_shortener.repository.url_shortener_repository import UrlShortenerRepository
from url_shortener.web.api.schemas import UrlShortenRequest
from url_shortener.shortener_service.shortener_service import UrlShortenerService


router = APIRouter()


@router.get("/{short_url}")
def redirect_to_long_url(short_url: str):
    """Redirect to the original URL."""
    print(short_url)


@router.post("/")
def shorten_url(long_url: UrlShortenRequest):
    """Shorten the given URL."""
    with UnitOfWork() as unit_of_work:
        repo = UrlShortenerRepository(unit_of_work.session)
        url_shortener_service = UrlShortenerService(repo)
        shortened_url = url_shortener_service.shorten_url(long_url.url)
        unit_of_work.commit()
        print(shortened_url)
        return_payload = shortened_url.dict()

    return return_payload
