"""APIs for the URL shortener app."""

import os
from typing import Annotated
import requests

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from url_shortener.repository.unit_of_work import UnitOfWork
from url_shortener.repository.url_shortener_repository import UrlShortenerRepository
from url_shortener.web.api.schemas import (
    UrlShortenRequest,
    GetShortenedUrlSchema,
    Token,
)
from url_shortener.shortener_service.shortener_service import UrlShortenerService
from url_shortener.shortener_service.shortener import UrlShortener
from url_shortener.repository.redis_repository import UrlShortenerRedisRepository
from url_shortener.exceptions import credentials_exception

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Get the access token for the user from the authentication service, 
    only for testing purposes, not used in production
    """

    username = form_data.username
    password = form_data.password

    if username is None or password is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username or password missing",
        )

    auth_service_url = os.getenv("LOCAL_DEV_AUTH_SERVICE_URL")
    payload = f"username={username}&password={password}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.request("POST", auth_service_url, headers=headers, data=payload, timeout=20)
    response_dict = response.json()

    return Token(**response_dict)


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
    "/shorten_url",
    status_code=status.HTTP_201_CREATED,
    response_model=GetShortenedUrlSchema,
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


@router.post(
    "/shorten_url_auth",
    status_code=status.HTTP_201_CREATED,
    response_model=GetShortenedUrlSchema,
)
def shorten_url_auth(
    long_url: UrlShortenRequest, token: Annotated[str, Depends(oauth2_scheme)]
) -> GetShortenedUrlSchema:
    """Shorten URLs for logged in users"""

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), os.getenv("ALGORITHM"))
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    with UnitOfWork() as unit_of_work:
        repo: UrlShortenerRepository = UrlShortenerRepository(unit_of_work.session)
        cache: UrlShortenerRedisRepository = UrlShortenerRedisRepository(
            unit_of_work.redis_connection
        )
        url_shortener_service: UrlShortenerService = UrlShortenerService(repo)
        shortened_url: UrlShortener = url_shortener_service.shorten_url(
            long_url.url, username
        )
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


@router.get("/health/api_health", status_code=status.HTTP_200_OK)
def api_health_check():
    """Health check for the API"""
    return {
        "API Status": "Online",
        "Pod Name": os.getenv("HOSTNAME", default="local"),
    }
