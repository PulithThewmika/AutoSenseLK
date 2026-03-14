"""
Dependency injection helpers for FastAPI.
- DB session management
- Authentication / authorization dependencies
"""

from typing import Generator

# from sqlalchemy.orm import Session
# from app.core.database import SessionLocal
# from app.core.security import verify_api_key


def get_db():  # -> Generator[Session, None, None]:
    """Yield a DB session and ensure it is closed after the request."""
    # db = SessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()
    ...


def get_current_user():
    """Validate the API key / JWT and return the current user or raise 401."""
    # token = ...
    # return verify_api_key(token)
    ...
