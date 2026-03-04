"""
Pydantic schemas for data validation and API responses.
"""

from datetime import datetime, date           # Standard: Date types
from typing import Optional, List             # Standard: Type hinting
from pydantic import BaseModel, ConfigDict    # Third Party: Validation


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


class CategoryUpdate(BaseModel):
    """
    Data for updating a category.
    """
    name: Optional[str] = None


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
    logo_url: Optional[str] = None  # Added here so it's inherited


class ManufacturerCreate(ManufacturerBase):
    """
    Data required to create a manufacturer linked to a category.
    """
    category_id: int


class ManufacturerUpdate(BaseModel):
    """
    Data for updating a manufacturer.
    """
    name: Optional[str] = None
    category_id: Optional[int] = None
    logo_url: Optional[str] = None  # Added for updates


class Manufacturer(ManufacturerBase):
    """
    The full Manufacturer schema as returned by the API.
    """
    id: int
    category_id: int
    logo_url: Optional[str] = None  # Added to the response
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


class AircraftModelUpdate(BaseModel):
    """
    Data for updating an aircraft model (all fields optional).
    """
    name: Optional[str] = None
    passengers: Optional[str] = None
    max_takeoff_weight: Optional[str] = None
    max_landing_weight: Optional[str] = None
    max_fuel_capacity: Optional[str] = None
    max_range: Optional[str] = None
    max_ceiling: Optional[str] = None
    max_cruising_speed: Optional[str] = None
    thrust_power: Optional[str] = None
    manufacturer_id: Optional[int] = None


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
    pilot_name: Optional[str] = None
    airline: Optional[str] = None
    groundspeed: float
    flight_date: Optional[date] = None  # Pydantic handles ISO strings to dates
    description: Optional[str] = None   # Notes


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
