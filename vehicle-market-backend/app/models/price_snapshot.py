"""
Historical price snapshot ORM model.
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class PriceSnapshot(Base):
    """Daily snapshot of a listing's price for trend analysis."""

    __tablename__ = "price_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    price = Column(Float, nullable=False)
    captured_at = Column(DateTime(timezone=True), server_default=func.now())
