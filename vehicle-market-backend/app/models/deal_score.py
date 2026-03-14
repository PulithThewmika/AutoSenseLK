"""
Deal score ORM model — stores ML-generated score per listing.
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class DealScore(Base):
    """ML-predicted deal quality for a listing."""

    __tablename__ = "deal_scores"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), unique=True, nullable=False)
    predicted_price = Column(Float, nullable=False)
    actual_price = Column(Float, nullable=False)
    score = Column(Float, nullable=False)
    label = Column(String(20), nullable=False)  # good_deal / fair / overpriced
    scored_at = Column(DateTime(timezone=True), server_default=func.now())
