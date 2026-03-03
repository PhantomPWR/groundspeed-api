"""
Pydantic schemas for data validation and API responses.
"""

from pydantic import BaseModel, ConfigDict    # Third Party: Validation
from datetime import datetime                 # Standard: Date types
from typing import Optional, List             # Standard: Type hinting


# --- CATEGORY SCHEMAS ---

class CategoryBase(BaseModel):
    """
    Base properties for an aircraft category.
    """
    name: str


class CategoryCreate(CategoryBase):
    """
    Data required to create a new category.
    """
    pass


class Category(CategoryBase):
    """
    The full Category schema as returned by the API.
    """
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- MANUFACTURER SCHEMAS ---

class ManufacturerBase(BaseModel):
    """
    Base properties for a manufacturer.
    """
    name: str


class ManufacturerCreate(ManufacturerBase):
    """
    Data required to create a manufacturer linked to a category.
    """
    category_id: int


class Manufacturer(ManufacturerBase):
    """
    The full Manufacturer schema as returned by the API.
    """
    id: int
    category_id: int
    model_config = ConfigDict(from_attributes=True)


# --- AIRCRAFT MODEL SCHEMAS ---

class AircraftModelBase(BaseModel):
    """
    Base properties for an aircraft model including technical specs.
    """
    name: str
    passengers: Optional[str] = "-"
    max_takeoff_weight: Optional[str] = "-"
    max_landing_weight: Optional[str] = "-"
    max_fuel_capacity: Optional[str] = "-"
    max_range: Optional[str] = "-"
    max_ceiling: Optional[str] = "-"
    max_cruising_speed: Optional[str] = "-"
    thrust_power: Optional[str] = "-"


class AircraftModelCreate(AircraftModelBase):
    """
    Data required to create a model, linked to a manufacturer.
    """
    manufacturer_id: int


class AircraftModel(AircraftModelBase):
    """
    The full Aircraft Model schema as returned by the API.
    """
    id: int
    image_url: Optional[str] = None
    manufacturer_id: int
    model_config = ConfigDict(from_attributes=True)


# --- SPEED RECORD SCHEMAS ---

class SpeedRecordBase(BaseModel):
    """
    Base properties for a groundspeed record.
    """
    pilot_name: str
    groundspeed: float
    description: Optional[str] = None


class SpeedRecordCreate(SpeedRecordBase):
    """
    Data required to submit a new record.
    """
    model_id: int


class SpeedRecord(SpeedRecordBase):
    """
    The full Speed Record schema as returned by the API.
    """
    id: int
    photo_url: str
    created_at: datetime
    model_id: int
    model_config = ConfigDict(from_attributes=True)
