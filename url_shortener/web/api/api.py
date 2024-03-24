"""APIs for the URL shortener app."""

from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from url_shortener.repository.unit_of_work import UnitOfWork
from url_shortener.repository.url_shortener_repository import UrlShortenerRepository
from url_shortener.web.api.schemas import UrlShortenRequest, GetShortenedUrlSchema
from url_shortener.shortener_service.shortener_service import UrlShortenerService
from url_shortener.shortener_service.shortener import UrlShortener
from url_shortener.repository.redis_repository import UrlShortenerRedisRepository


router = APIRouter()


@router.get("/{short_url}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def redirect_to_long_url(short_url: str):
    """Redirect to the original URL."""

    with UnitOfWork() as unit_of_work:
        cache: UrlShortenerRedisRepository = UrlShortenerRedisRepository(
            unit_of_work.redis_connection
        )
        repo: UrlShortenerRepository = UrlShortenerRepository(unit_of_work.session)
        url_shortener_service: UrlShortenerService = UrlShortenerService(repo)

        long_url: str = cache.get(short_url)

        if long_url:
            print("Cache hit")
            redirect = RedirectResponse(
                url=long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
            )
            return redirect

        long_url: UrlShortener = url_shortener_service.get_long_url(short_url)
        unit_of_work.commit()

    if long_url:
        redirect = RedirectResponse(
            url=long_url.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
        return redirect

    return {"message": "URL not found."}


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=GetShortenedUrlSchema
)
def shorten_url(long_url: UrlShortenRequest) -> GetShortenedUrlSchema:
    """Shorten the given URL."""
    with UnitOfWork() as unit_of_work:
        repo: UrlShortenerRepository = UrlShortenerRepository(unit_of_work.session)
        cache: UrlShortenerRedisRepository = UrlShortenerRedisRepository(
            unit_of_work.redis_connection
        )
        url_shortener_service: UrlShortenerService = UrlShortenerService(repo)
        shortened_url: UrlShortener = url_shortener_service.shorten_url(long_url.url)
        unit_of_work.commit()
        cache.set(shortened_url.short_url, shortened_url.long_url)

        return_payload: GetShortenedUrlSchema = shortened_url.dict()

    return return_payload


@router.get("/health/storage_health", status_code=status.HTTP_200_OK)
def storage_health_check():
    """Health check for in-memory and persistence storage"""
    with UnitOfWork() as unit_of_work:
        cache: UrlShortenerRedisRepository = UrlShortenerRedisRepository(
            unit_of_work.redis_connection
        )
        repo: UrlShortenerRepository = UrlShortenerRepository(unit_of_work.session)
        health_check = {
            "Database Status": "Online" if repo.check_health() else "Offline",
            "Cache Status": "Online" if cache.ping() else "Offline",
        }
        unit_of_work.commit()

    return health_check
