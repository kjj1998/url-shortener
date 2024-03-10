"""URL shortener repository"""

from url_shortener.repository.models import UrlModel
from url_shortener.shortener_service.shortener import UrlShortener


class UrlShortenerRepository:
    """URL shortener repository"""

    def __init__(self, session):
        self.session = session

    def add(self, long_url, short_url) -> UrlShortener:
        """Add a new URL to the database."""
        record = UrlModel(long_url=long_url, short_url=short_url)
        self.session.add(record)
        self.session.commit()

        return UrlShortener(**record.dict())

    def get_long_url(self, short_url) -> UrlShortener:
        """Get the original URL for the given short URL."""
        url_model: UrlModel = (
            self.session.query(UrlModel).filter(UrlModel.short_url == short_url).first()
        )

        if url_model is not None:
            return UrlShortener(**url_model.dict())

        return None
