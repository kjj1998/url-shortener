"""URL shortener service"""

from pydantic import AnyUrl
from snowflake import SnowflakeGenerator
import base62

from url_shortener.repository.url_shortener_repository import UrlShortenerRepository


class UrlShortenerService:
    """Service to shorten URLs."""

    def __init__(self, url_shortener_repository: UrlShortenerRepository):
        self.url_shortener_repository = url_shortener_repository

    def shorten_url(self, long_url: AnyUrl):
        """Shorten the given URL."""

        if long_url is not None:
            gen = SnowflakeGenerator(42)
            unique_id = next(gen)
            short_url = base62.encode(unique_id)
            return self.url_shortener_repository.add(str(long_url), short_url)

    def get_long_url(self, short_url):
        """Get the original URL for the given short URL."""
        pass
