"""
Vehicle Make / Model / Year ORM models.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Make(Base):
    """Vehicle manufacturer (e.g. Toyota, Honda)."""

    __tablename__ = "makes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    models = relationship("Model", back_populates="make")


class Model(Base):
    """Vehicle model belonging to a make (e.g. Corolla, Civic)."""

    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    make_id = Column(Integer, ForeignKey("makes.id"), nullable=False)

    make = relationship("Make", back_populates="models")
