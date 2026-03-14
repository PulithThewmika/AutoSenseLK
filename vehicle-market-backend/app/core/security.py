"""
Security helpers — API key validation and JWT token utilities.
"""

from datetime import datetime, timedelta, timezone

# from jose import JWTError, jwt
# from app.core.config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generate a signed JWT access token."""
    # to_encode = data.copy()
    # expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    # to_encode.update({"exp": expire})
    # return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    ...


def verify_api_key(api_key: str) -> bool:
    """Check whether the provided API key is valid."""
    # return api_key == settings.API_KEY
    ...
