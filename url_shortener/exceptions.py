"""Exceptions"""

from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

authentication_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

username_wrong_match_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="username given does not match with username from token",
    headers={"WWW-Authenticate": "Bearer"},
)

shortened_url_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Shortened URL not found",
)
