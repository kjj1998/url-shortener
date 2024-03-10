"""APIs for the URL shortener app."""

from fastapi import APIRouter

from url_shortener.repository.unit_of_work import UnitOfWork
from url_shortener.repository.url_shortener_repository import UrlShortenerRepository
from url_shortener.web.api.schemas import UrlShortenRequest, GetShortenedUrlSchema
from url_shortener.shortener_service.shortener_service import UrlShortenerService
from url_shortener.shortener_service.shortener import UrlShortener


router = APIRouter()


@router.get("/{short_url}")
def redirect_to_long_url(short_url: str):
    """Redirect to the original URL."""
    print(short_url)


@router.post("/",  response_model=GetShortenedUrlSchema)
def shorten_url(long_url: UrlShortenRequest) -> GetShortenedUrlSchema:
    """Shorten the given URL."""
    with UnitOfWork() as unit_of_work:
        repo: UrlShortenerRepository = UrlShortenerRepository(unit_of_work.session)
        url_shortener_service: UrlShortenerService = UrlShortenerService(repo)
        shortened_url: UrlShortener = url_shortener_service.shorten_url(long_url.url)
        unit_of_work.commit()
        return_payload: GetShortenedUrlSchema = shortened_url.dict()

    return return_payload
