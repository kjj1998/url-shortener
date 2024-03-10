"""APIs for the URL shortener app."""

from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from url_shortener.repository.unit_of_work import UnitOfWork
from url_shortener.repository.url_shortener_repository import UrlShortenerRepository
from url_shortener.web.api.schemas import UrlShortenRequest, GetShortenedUrlSchema
from url_shortener.shortener_service.shortener_service import UrlShortenerService
from url_shortener.shortener_service.shortener import UrlShortener


router = APIRouter()


@router.get("/{short_url}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def redirect_to_long_url(short_url: str):
    """Redirect to the original URL."""

    with UnitOfWork() as unit_of_work:
        repo: UrlShortenerRepository = UrlShortenerRepository(unit_of_work.session)
        url_shortener_service: UrlShortenerService = UrlShortenerService(repo)
        long_url: UrlShortener = url_shortener_service.get_long_url(short_url)
        unit_of_work.commit()

    if long_url:
        redirect = RedirectResponse(
            url=long_url.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
        return redirect


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=GetShortenedUrlSchema
)
def shorten_url(long_url: UrlShortenRequest) -> GetShortenedUrlSchema:
    """Shorten the given URL."""
    with UnitOfWork() as unit_of_work:
        repo: UrlShortenerRepository = UrlShortenerRepository(unit_of_work.session)
        url_shortener_service: UrlShortenerService = UrlShortenerService(repo)
        shortened_url: UrlShortener = url_shortener_service.shorten_url(long_url.url)
        unit_of_work.commit()
        return_payload: GetShortenedUrlSchema = shortened_url.dict()

    return return_payload
