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

    def get_urls_by_user(self, username) -> list[UrlShortener]:
        """Get all URLs for the given user."""
        url_models = (
            self.session.query(UrlModel).filter(UrlModel.username == username).all()
        )

        urls = []
        for url in url_models:
            urls.append(UrlShortener(**url.dict()))

        return urls

    def delete_shortened_url_for_user(self, url_id, username):
        """Delete a shortened URL for the user"""
        url_model: UrlModel = (
            self.session.query(UrlModel)
            .filter(UrlModel.id == url_id, UrlModel.username == username)
            .first()
        )

        if url_model is not None:
            self.session.delete(url_model)
            self.session.commit()
        else:
            raise Exception("URL not found")
