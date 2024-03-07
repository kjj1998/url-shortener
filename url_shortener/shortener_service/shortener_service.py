"""URL shortener service"""

from pydantic import AnyUrl
from snowflake import SnowflakeGenerator
import base62

class UrlShortenerService:
    """Service to shorten URLs."""

    def __init__(self):
        pass

    def shorten_url(self, long_url: AnyUrl):
        """Shorten the given URL."""
        gen = SnowflakeGenerator(42)
        unique_id = next(gen)
        base62_id = base62.encode(unique_id)

        print(base62_id)



    def get_long_url(self, short_url):
        """Get the original URL for the given short URL."""
        pass
