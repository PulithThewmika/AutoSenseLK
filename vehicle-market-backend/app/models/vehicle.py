"""
Vehicle Make / Model document models (Beanie / MongoDB).
"""

from typing import Optional

from beanie import Document


class Make(Document):
    """Vehicle manufacturer (e.g. Toyota, Honda)."""

    name: str

    class Settings:
        name = "makes"
        indexes = ["name"]


class Model(Document):
    """Vehicle model belonging to a make (e.g. Corolla, Civic)."""

    name: str
    make_id: str  # Reference to Make document ID

    class Settings:
        name = "models"
        indexes = ["name", "make_id"]
