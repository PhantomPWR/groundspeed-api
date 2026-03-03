"""
Aircraft management endpoints for categories, manufacturers, and models.
"""

from typing import List                 # Standard: Type hinting
from fastapi import APIRouter, Depends  # Third Party: Core routing & DI
from sqlalchemy.orm import Session      # Third Party: DB session typing

# Local: Using absolute imports starting from the 'app' directory
from app import crud, schemas           
from app.database import get_db

router = APIRouter(
    prefix="/aircraft",
    tags=["Aircraft Management"]
)


@router.get("/categories", response_model=List[schemas.Category])
def read_categories(db: Session = Depends(get_db)):
    """
    Returns a list of all aircraft categories.
    """
    return crud.get_categories(db)


@router.post("/categories", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate, 
    db: Session = Depends(get_db)
):
    """
    Creates a new aircraft category.
    """
    return crud.create_category(db=db, category=category)


@router.get("/manufacturers", response_model=List[schemas.Manufacturer])
def read_manufacturers(category_id: int = None, db: Session = Depends(get_db)):
    """
    Returns manufacturers, optionally filtered by category.
    """
    return crud.get_manufacturers(db, category_id=category_id)


@router.post("/manufacturers", response_model=schemas.Manufacturer)
def create_manufacturer(
    manufacturer: schemas.ManufacturerCreate, 
    db: Session = Depends(get_db)
):
    """
    Creates a manufacturer linked to a category.
    """
    return crud.create_manufacturer(db=db, manufacturer=manufacturer)


@router.get("/models", response_model=List[schemas.AircraftModel])
def read_models(manufacturer_id: int = None, db: Session = Depends(get_db)):
    """
    Returns aircraft models, optionally filtered by manufacturer.
    """
    return crud.get_aircraft_models(db, manufacturer_id=manufacturer_id)


@router.post("/models", response_model=schemas.AircraftModel)
def create_aircraft_model(
    aircraft_model: schemas.AircraftModelCreate, 
    db: Session = Depends(get_db)
):
    """
    Creates an aircraft model linked to a manufacturer.
    """
    return crud.create_aircraft_model(db=db, aircraft_model=aircraft_model)
