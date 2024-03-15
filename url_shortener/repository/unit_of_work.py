"""Unit of work pattern implementation."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

parent_directory_path = os.path.dirname(os.getcwd())
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)

db_host = os.getenv("DB_HOST_DOCKER") if os.getenv("DB_HOST_DOCKER") else os.getenv("DB_HOST_LOCAL")

DB_URL = f"postgresql://admin:password@{db_host}:5432/urlshortener"

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
