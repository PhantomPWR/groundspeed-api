"""
Aircraft management endpoints for categories, manufacturers, and models.
"""

import shutil                                 # Standard: File operations
from typing import List, Optional             # Standard: Type hinting
from fastapi import (                         # Third Party: Web tools
    APIRouter, Depends, HTTPException,
    status, Form, UploadFile, File
)
from sqlalchemy.orm import Session            # Third Party: DB session
from app import crud, schemas, models, utils  # Local: App modules
from app.database import get_db               # Local: DB connection helper


class AircraftForm:
    """
    Dependency class to group aircraft form fields.
    This resolves Pylint 'too-many-arguments' warnings.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        name: str = Form(...),
        manufacturer_id: int = Form(...),
        passengers: str = Form("-"),
        max_takeoff_weight: str = Form("-"),
        max_landing_weight: str = Form("-"),
        max_fuel_capacity: str = Form("-"),
        max_range: str = Form("-"),
        max_ceiling: str = Form("-"),
        max_cruising_speed: str = Form("-"),
        thrust_power: str = Form("-"),
    ):
        self.name = name
        self.manufacturer_id = manufacturer_id
        self.passengers = passengers
        self.max_takeoff_weight = max_takeoff_weight
        self.max_landing_weight = max_landing_weight
        self.max_fuel_capacity = max_fuel_capacity
        self.max_range = max_range
        self.max_ceiling = max_ceiling
        self.max_cruising_speed = max_cruising_speed
        self.thrust_power = thrust_power


router = APIRouter(
    prefix="/aircraft",
    tags=["Aircraft Management"]
)


# --- CATEGORY ROUTES ---

@router.get("/categories", response_model=List[schemas.Category])
def read_categories(db: Session = Depends(get_db)):
    """Returns all categories."""
    return crud.get_categories(db)


@router.post(
    "/categories",
    response_model=schemas.Category,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """Creates a new category."""
    return crud.create_category(db=db, category=category)


@router.put("/categories/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """Updates an existing category's name."""
    db_cat = crud.update_category(db, category_id, category)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_cat


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Deletes a category by ID."""
    success = crud.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return None


# --- MANUFACTURER ROUTES ---

@router.get("/manufacturers", response_model=List[schemas.Manufacturer])
def read_manufacturers(category_id: int = None, db: Session = Depends(get_db)):
    """Returns manufacturers, optionally filtered by category."""
    return crud.get_manufacturers(db, category_id=category_id)


@router.post("/manufacturers", response_model=schemas.Manufacturer)
def create_manufacturer(
    manufacturer: schemas.ManufacturerCreate,
    db: Session = Depends(get_db)
):
    """Creates a manufacturer linked to a category."""
    return crud.create_manufacturer(db=db, manufacturer=manufacturer)


@router.put("/manufacturers/{manufacturer_id}", response_model=schemas.Manufacturer)
def update_manufacturer(
    manufacturer_id: int,
    manufacturer: schemas.ManufacturerCreate,
    db: Session = Depends(get_db)
):
    """Updates a manufacturer's name or category."""
    db_man = crud.update_manufacturer(db, manufacturer_id, manufacturer)
    if not db_man:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return db_man


@router.delete("/manufacturers/{manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_manufacturer(manufacturer_id: int, db: Session = Depends(get_db)):
    """Deletes a manufacturer by ID."""
    success = crud.delete_manufacturer(db, manufacturer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return None


# --- AIRCRAFT MODEL ROUTES ---

@router.get("/models", response_model=List[schemas.AircraftModel])
def read_models(manufacturer_id: int = None, db: Session = Depends(get_db)):
    """Returns aircraft models, optionally filtered by manufacturer."""
    return crud.get_aircraft_models(db, manufacturer_id=manufacturer_id)


@router.post("/models", response_model=schemas.AircraftModel)
async def create_aircraft_model(
    form: AircraftForm = Depends(),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Creates a new aircraft model using the AircraftForm dependency.
    """
    # 1. Fetch Manufacturer & Category to build the filename
    man = db.query(models.Manufacturer).filter(
        models.Manufacturer.id == form.manufacturer_id
    ).first()
    
    if not man:
        raise HTTPException(status_code=404, detail="Manufacturer not found")

    # 2. Handle optional image upload
    image_path = None
    if image:
        fn = utils.generate_aircraft_image_filename(
            category=man.category.name,
            manufacturer=man.name,
            model=form.name,
            original_filename=image.filename
        )
        image_path = f"static/uploads/{fn}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    # 3. Map form data to creation schema
    model_data = schemas.AircraftModelCreate(
        name=form.name,
        manufacturer_id=form.manufacturer_id,
        passengers=form.passengers,
        max_takeoff_weight=form.max_takeoff_weight,
        max_landing_weight=form.max_landing_weight,
        max_fuel_capacity=form.max_fuel_capacity,
        max_range=form.max_range,
        max_ceiling=form.max_ceiling,
        max_cruising_speed=form.max_cruising_speed,
        thrust_power=form.thrust_power
    )

    return crud.create_aircraft_model(
        db=db, aircraft_model=model_data, image_url=image_path
    )
