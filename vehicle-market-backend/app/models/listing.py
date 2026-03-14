"""
Listing ORM model.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class Listing(Base):
    """A single vehicle listing scraped from the marketplace."""

    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="LKR")
    mileage = Column(Float, nullable=True)
    year = Column(Integer, nullable=True)
    location = Column(String(255), nullable=True)
    source_url = Column(String(512), unique=True, nullable=False)
    source_hash = Column(String(64), unique=True, nullable=False)
    make_id = Column(Integer, ForeignKey("makes.id"), nullable=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
