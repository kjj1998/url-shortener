"""URL shortener service"""

from pydantic import AnyUrl
from snowflake import SnowflakeGenerator
import base62

from url_shortener.repository.url_shortener_repository import UrlShortenerRepository
from url_shortener.shortener_service.shortener import UrlShortener


class UrlShortenerService:
    """Service to shorten URLs."""

    def __init__(self, url_shortener_repository: UrlShortenerRepository):
        self.url_shortener_repository: UrlShortenerRepository = url_shortener_repository

    def shorten_url(self, long_url: AnyUrl, username: str | None = None) -> UrlShortener:
        """Shorten the given URL."""

        if long_url is not None:
            gen: SnowflakeGenerator = SnowflakeGenerator(42)
            unique_id: str = next(gen)
            short_url: str = base62.encode(unique_id)
            return self.url_shortener_repository.add(str(long_url), short_url, username)

        # Raise exception for invalid URL

    def get_long_url(self, short_url) -> UrlShortener:
        """Get the original URL for the given short URL."""

        if short_url is not None:
            return self.url_shortener_repository.get_long_url(short_url)

        # Raise exception for invalid URL

    def get_urls_by_user(self, username) -> list[UrlShortener]:
        """Get all URLs for the given user."""

        if username is not None:
            return self.url_shortener_repository.get_urls_by_user(username)