"""URL shortener repository"""

from sqlalchemy.exc import DatabaseError
from sqlalchemy.sql import text

from url_shortener.repository.models import UrlModel
from url_shortener.shortener_service.shortener import UrlShortener

class UrlShortenerRepository:
    """URL shortener repository"""

    def __init__(self, session):
        self.session = session

    def add(self, long_url, short_url, username) -> UrlShortener:
        """Add a new URL to the database."""
        record = UrlModel(long_url=long_url, short_url=short_url, username=username)
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

    def check_health(self):
        """Check the health of the database."""
        try:
            self.session.execute(text("SELECT 1"))
            return True
        except DatabaseError as e:
            print("Database:", e)
            return False
