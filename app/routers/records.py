"""
Endpoints for submitting and retrieving groundspeed records.
"""

import os                                     # Standard: OS tools
import shutil                                 # Standard: File operations
from datetime import date                     # Standard: Date type (FIXED)
from typing import List, Optional             # Standard: Type hinting
from fastapi import (                         # Third Party: Web tools
    APIRouter, Depends, HTTPException,
    UploadFile, File, Form, status
)
from sqlalchemy.orm import Session            # Third Party: DB session
from app import crud, models, schemas, utils  # Local: App modules
from app.database import get_db               # Local: DB connection helper


class RecordForm:
    """
    Dependency class to group record form fields for creation.
    """
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        groundspeed: float = Form(...),
        model_id: int = Form(...),
        pilot_name: Optional[str] = Form(None),
        airline: Optional[str] = Form(None),
        flight_date: Optional[date] = Form(None),
        description: Optional[str] = Form(None),
    ):
        self.groundspeed = groundspeed
        self.model_id = model_id
        self.pilot_name = pilot_name
        self.airline = airline
        self.flight_date = flight_date
        self.description = description


class RecordUpdateForm:
    """
    Dependency class to group record form fields for updates.
    """
    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        groundspeed: Optional[float] = Form(None),
        model_id: Optional[int] = Form(None),
        pilot_name: Optional[str] = Form(None),
        airline: Optional[str] = Form(None),
        flight_date: Optional[date] = Form(None),
        description: Optional[str] = Form(None)
    ):
        self.groundspeed = groundspeed
        self.model_id = model_id
        self.pilot_name = pilot_name
        self.airline = airline
        self.flight_date = flight_date
        self.description = description


router = APIRouter(
    prefix="/records",
    tags=["Speed Records"]
)


@router.get("/", response_model=List[schemas.SpeedRecord])
def read_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns a paginated list of speed records.
    """
    return crud.get_records(db, skip=skip, limit=limit)


@router.get("/{record_id}", response_model=schemas.SpeedRecord)
def read_record(record_id: int, db: Session = Depends(get_db)):
    """
    Returns a single groundspeed record by ID.
    """
    db_record = crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record


@router.post(
    "/",
    response_model=schemas.SpeedRecord,
    status_code=status.HTTP_201_CREATED
)
async def create_record(
    form: RecordForm = Depends(),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Handles submission of a record including custom-named photo save.
    """
    model = db.query(models.AircraftModel).filter(
        models.AircraftModel.id == form.model_id
    ).first()

    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    new_fn = utils.generate_record_filename(
        category=model.manufacturer.category.name,
        manufacturer=model.manufacturer.name,
        model=model.name,
        speed=form.groundspeed,
        original_filename=photo.filename
    )

    file_path = f"static/uploads/{new_fn}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    record_data = schemas.SpeedRecordCreate(
        pilot_name=form.pilot_name,
        airline=form.airline,
        groundspeed=form.groundspeed,
        flight_date=form.flight_date,
        model_id=form.model_id,
        description=form.description
    )

    return crud.create_speed_record(
        db=db, record=record_data, photo_url=file_path
    )


@router.put("/{record_id}", response_model=schemas.SpeedRecord)
async def update_record(
    record_id: int,
    form: RecordUpdateForm = Depends(),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Updates a speed record's details and optional proof photo.
    """
    db_record = crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    photo_path = None
    if photo:
        if db_record.photo_url and os.path.exists(db_record.photo_url):
            os.remove(db_record.photo_url)
            
        mid = form.model_id or db_record.model_id
        model = db.query(models.AircraftModel).filter(
            models.AircraftModel.id == mid
        ).first()
        
        new_fn = utils.generate_record_filename(
            category=model.manufacturer.category.name,
            manufacturer=model.manufacturer.name,
            model=model.name,
            speed=form.groundspeed or db_record.groundspeed,
            original_filename=photo.filename
        )
        photo_path = f"static/uploads/{new_fn}"
        
        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

    update_data = schemas.SpeedRecordBase(
        pilot_name=form.pilot_name,
        airline=form.airline,
        groundspeed=form.groundspeed,
        flight_date=form.flight_date,
        description=form.description
    )

    return crud.update_speed_record(
        db=db, 
        record_id=record_id,
        record_update=update_data,
        photo_url=photo_path
    )


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    """
    Deletes a record and its associated image file.
    """
    db_record = crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    if db_record.photo_url and os.path.exists(db_record.photo_url):
        os.remove(db_record.photo_url)

    crud.delete_speed_record(db, record_id)
    return None
