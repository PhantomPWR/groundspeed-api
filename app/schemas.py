from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List


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


class ManufacturerBase(BaseModel):
    """
    Base properties for a manufacturer.
    """
    name: str


class ManufacturerCreate(ManufacturerBase):
    """
    Data required to create a manufacturer, linked to a category.
    """
    category_id: int


class Manufacturer(ManufacturerBase):
    """
    The full Manufacturer schema as returned by the API.
    """
    id: int
    category_id: int
    model_config = ConfigDict(from_attributes=True)


class AircraftModelBase(BaseModel):
    """
    Base properties for an aircraft model.
    """
    name: str


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
    manufacturer_id: int
    model_config = ConfigDict(from_attributes=True)


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
    Note: The photo is handled as a separate file upload.
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