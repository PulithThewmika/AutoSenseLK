"""
Dependency injection helpers for FastAPI.
- Authentication / authorization dependencies
"""

# from app.core.security import verify_api_key


def get_current_user():
    """Validate the API key / JWT and return the current user or raise 401."""
    # token = ...
    # return verify_api_key(token)
    ...
