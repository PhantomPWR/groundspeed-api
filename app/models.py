"""
SQLAlchemy database models for the Groundspeed Records application.
"""

import datetime                     # Standard: Date and time utilities
from sqlalchemy import (            # Third Party: Database column types
    Column, Integer, String, 
    Float, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship # Third Party: Model relationships
from app.database import Base       # Local: Base class for models


class Category(Base):
    """
    Represents the top-level classification of aircraft.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    # Relationships
    manufacturers = relationship("Manufacturer", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"


class Manufacturer(Base):
    """
    Represents an aircraft manufacturer.
    """
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Relationships
    category = relationship("Category", back_populates="manufacturers")
    aircraft_models = relationship(
        "AircraftModel", back_populates="manufacturer"
    )

    def __repr__(self):
        return f"<Manufacturer {self.name}>"


class AircraftModel(Base):
    """
    Represents a specific aircraft model and its technical specifications.
    """
    __tablename__ = "aircraft_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_url = Column(String, nullable=True)
    
    # Technical Specifications
    passengers = Column(String, nullable=True)
    max_takeoff_weight = Column(String, nullable=True)
    max_landing_weight = Column(String, nullable=True)
    max_fuel_capacity = Column(String, nullable=True)
    max_range = Column(String, nullable=True)
    max_ceiling = Column(String, nullable=True)
    max_cruising_speed = Column(String, nullable=True)
    thrust_power = Column(String, nullable=True)

    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))

    # Relationships
    manufacturer = relationship(
        "Manufacturer", back_populates="aircraft_models"
    )
    records = relationship("SpeedRecord", back_populates="aircraft_model")

    def __repr__(self):
        return f"<AircraftModel {self.name}>"


class SpeedRecord(Base):
    """
    Represents an individual groundspeed record submitted by a pilot.
    """
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    pilot_name = Column(String)
    groundspeed = Column(Float)
    photo_url = Column(String)
    description = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    model_id = Column(Integer, ForeignKey("aircraft_models.id"))

    # Relationships
    aircraft_model = relationship("AircraftModel", back_populates="records")

    def __repr__(self):
        return f"<SpeedRecord {self.pilot_name}: {self.groundspeed}kts>"
