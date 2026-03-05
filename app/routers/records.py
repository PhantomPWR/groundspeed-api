"""
Endpoints for submitting and retrieving groundspeed records.
"""

import os                                     # Standard: OS tools
import shutil                                 # Standard: File operations
from datetime import date                     # Standard: Date type
from typing import List, Optional             # Standard: Type hinting
from fastapi import (                         # Third Party: Web tools
    APIRouter, Depends, HTTPException,
    UploadFile, File, Form, status
)
from sqlalchemy.orm import Session            # Third Party: DB session
from app import crud, models, schemas, utils  # Local: App modules
from app.database import get_db               # Local: DB connection helper
from app.dependencies import (                # Local: Auth dependencies
    get_current_user, get_current_active_admin
)


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
        description: Optional[str] = Form(None)
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
def read_records(
    model_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Returns a paginated list of speed records. Public access.
    """
    query = db.query(models.SpeedRecord)
    if model_id:
        query = query.filter(models.SpeedRecord.model_id == model_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{record_id}", response_model=schemas.SpeedRecord)
def read_record(record_id: int, db: Session = Depends(get_db)):
    """
    Returns a single groundspeed record by ID. Public access.
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
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Handles submission of a record. Restricted to registered users.
    """
    model = db.query(models.AircraftModel).filter(
        models.AircraftModel.id == form.model_id
    ).first()

    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    # Generate professional filename
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

    # Link the record to the current user
    record_data = schemas.SpeedRecordCreate(
        **form.__dict__,
        user_id=current_user.id
    )

    return crud.create_speed_record(
        db=db, record=record_data, photo_url=file_path
    )


@router.put("/{record_id}", response_model=schemas.SpeedRecord)
async def update_record(
    record_id: int,
    form: RecordUpdateForm = Depends(),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Updates a record. Users can only update their own records.
    Admin/Owner can update any record.
    """
    db_record = crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Check Ownership/Permissions
    is_authorized = (
        current_user.role in ["owner", "admin"] or
        db_record.user_id == current_user.id
    )
    if not is_authorized:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to edit this record"
        )

    photo_path = None
    if photo:
        if db_record.photo_url and os.path.exists(db_record.photo_url):
            os.remove(db_record.photo_url)

        mid = form.model_id or db_record.model_id
        model = db.query(models.AircraftModel).get(mid)

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

    update_data = schemas.SpeedRecordBase(**form.__dict__)

    return crud.update_speed_record(
        db=db,
        record_id=record_id,
        record_update=update_data,
        photo_url=photo_path
    )


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_active_admin)
):
    """
    Deletes a record and its photo. Restricted to Admin/Owner.
    """
    db_record = crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    if db_record.photo_url and os.path.exists(db_record.photo_url):
        os.remove(db_record.photo_url)

    crud.delete_speed_record(db, record_id)
    return None
