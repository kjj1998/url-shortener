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
        try:
            return self.connection.ping()
        except RedisConnectionError as e:
            print("Redis:", e)
            return False

    def get(self, key: str) -> str:
        """Get the URL for the given key from the Redis cache."""
        try:
            return self.connection.get(key)
        except RedisConnectionError as e:
            print("Redis:", e)
            return None
