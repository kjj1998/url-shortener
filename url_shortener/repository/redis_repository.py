"""URL shortener Redis cache repository"""

from redis import Redis as redis
from redis.exceptions import ConnectionError as RedisConnectionError


class UrlShortenerRedisRepository:
    """URL shortener Redis cache repository"""

    def __init__(self, connection: redis):
        self.connection: redis = connection

    def set(self, key: str, url: str):
        """Set the key-url pair in the Redis cache."""
        try:
            self.connection.set(key, url)
        except RedisConnectionError as e:
            print("Redis:", e)

    def ping(self) -> bool:
        """Ping the Redis cache."""
        return self.connection.ping()

    def get(self, key: str) -> str:
        """Get the URL for the given key from the Redis cache."""
        try:
            return self.connection.get(key)
        except RedisConnectionError as e:
            print("Redis:", e)
            return None
        
    # def add(self, long_url, short_url) -> UrlShortener:
    #     """Add a new URL to the database."""
    #     record = UrlModel(long_url=long_url, short_url=short_url)
    #     self.session.add(record)
    #     self.session.commit()

    #     return UrlShortener(**record.dict())

    # def get_long_url(self, short_url) -> UrlShortener:
    #     """Get the original URL for the given short URL."""
    #     url_model: UrlModel = (
    #         self.session.query(UrlModel).filter(UrlModel.short_url == short_url).first()
    #     )

    #     if url_model is not None:
    #         return UrlShortener(**url_model.dict())

    #     return None
