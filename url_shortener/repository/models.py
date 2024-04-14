"""This module contains the models for the url shortener"""

from datetime import datetime
import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def generate_uuid() -> str:
    """function to generate uuid"""
    return str(uuid.uuid4())


class UrlModel(Base):  # pylint: disable=too-few-public-methods
    """Url sql model"""

    __table_args__ = {'schema' : 'shortener_schema'}
    __tablename__ = "url"

    id = Column(String, primary_key=True, default=generate_uuid)
    long_url = Column(String, nullable=False)
    short_url = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)

    def dict(self):
        """Render as dictionaries"""
        return {
            "id": self.id,
            "long_url": self.long_url,
            "short_url": self.short_url,
            "created": self.created,
        }
