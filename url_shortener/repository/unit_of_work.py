"""Unit of work pattern implementation."""

# import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://admin:password@localhost:5432/urlshortener"

assert DB_URL is not None, 'DB_URL environment variable needed.'


class UnitOfWork:
    """Unit of work pattern implementation."""

    def __init__(self):
        self.session_maker = sessionmaker(bind=create_engine(DB_URL))
        self.session = None

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()

    def commit(self):
        """commit the transaction"""
        self.session.commit()

    def rollback(self):
        """rollback the transaction"""
        self.session.rollback()
