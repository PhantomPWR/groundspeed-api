"""
Endpoints for submitting and retrieving groundspeed records.
"""

import shutil                       # Standard: File operations
from typing import List             # Standard: Type hinting
from fastapi import (               # Third Party: Web tools
    APIRouter, Depends, HTTPException,
    UploadFile, File, Form, status
)
from sqlalchemy.orm import Session  # Third Party: DB session typing

# Local: Absolute imports from the main 'app' package
from app import crud, models, schemas, utils 
from app.database import get_db

router = APIRouter(
    prefix="/records",
    tags=["Speed Records"]
)


@router.get("/", response_model=List[schemas.SpeedRecord])
def read_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Returns a paginated list of speed records."""
    return crud.get_records(db, skip=skip, limit=limit)


@router.post(
    "/", 
    response_model=schemas.SpeedRecord,
    status_code=status.HTTP_201_CREATED
)
async def create_record(
    pilot_name: str = Form(...),
    groundspeed: float = Form(...),
    model_id: int = Form(...),
    description: str = Form(None),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Handles submission of a record including custom-named photo save."""
    # 1. Lookup aircraft for name-building
    model = db.query(models.AircraftModel).filter(
        models.AircraftModel.id == model_id
    ).first()

    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    # 2. Build SEO-friendly filename using utils
    new_fn = utils.generate_record_filename(
        category=model.manufacturer.category.name,
        manufacturer=model.manufacturer.name,
        model=model.name,
        speed=groundspeed,
        original_filename=photo.filename
    )

    file_path = f"static/uploads/{new_fn}"

    # 3. Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # 4. Save to DB
    record_data = schemas.SpeedRecordCreate(
        pilot_name=pilot_name,
        groundspeed=groundspeed,
        model_id=model_id,
        description=description
    )

    return crud.create_speed_record(
        db=db, record=record_data, photo_url=file_path
    )
