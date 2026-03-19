"""
Vehicle Make / Model document models (Beanie / MongoDB).
"""

from typing import Optional

from beanie import Document


class Make(Document):
    """Vehicle manufacturer (e.g. Toyota, Honda)."""

    name: str              # Display name e.g. "Toyota"
    slug: str              # URL slug e.g. "toyota"
    scrape_url: str        # Brand-level ikman.lk listing URL

    class Settings:
        name = "makes"
        indexes = ["name", "slug"]


class Model(Document):
    """Vehicle model belonging to a make (e.g. Aqua, Civic)."""

    name: str              # Display name e.g. "Aqua"
    slug: str              # URL slug e.g. "aqua"
    make_slug: str         # Parent brand slug e.g. "toyota"
    scrape_url: str        # Model-level ikman.lk listing URL

    class Settings:
        name = "models"
        indexes = ["name", "slug", "make_slug", [("make_slug", 1), ("slug", 1)]]
