from sqlalchemy.orm import Session
from . import models, schemas


# --- CATEGORY CRUD ---

def get_categories(db: Session):
    """
    Fetches all aircraft categories from the database.
    """
    return db.query(models.Category).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    """
    Creates a new aircraft category.
    """
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# --- MANUFACTURER CRUD ---

def get_manufacturers(db: Session, category_id: int = None):
    """
    Fetches manufacturers, optionally filtered by category.
    """
    query = db.query(models.Manufacturer)
    if category_id:
        query = query.filter(models.Manufacturer.category_id == category_id)
    return query.all()


def create_manufacturer(db: Session, manufacturer: schemas.ManufacturerCreate):
    """
    Creates a new manufacturer linked to a category.
    """
    db_manufacturer = models.Manufacturer(
        name=manufacturer.name,
        category_id=manufacturer.category_id
    )
    db.add(db_manufacturer)
    db.commit()
    db.refresh(db_manufacturer)
    return db_manufacturer


# --- AIRCRAFT MODEL CRUD ---

def get_aircraft_models(db: Session, manufacturer_id: int = None):
    """
    Fetches aircraft models, optionally filtered by manufacturer.
    """
    query = db.query(models.AircraftModel)
    if manufacturer_id:
        query = query.filter(models.AircraftModel.manufacturer_id == manufacturer_id)
    return query.all()


def create_aircraft_model(db: Session, aircraft_model: schemas.AircraftModelCreate):
    """
    Creates a new aircraft model variant.
    """
    db_model = models.AircraftModel(
        name=aircraft_model.name,
        manufacturer_id=aircraft_model.manufacturer_id
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


# --- SPEED RECORD CRUD ---

def get_records(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches groundspeed records with pagination.
    """
    return db.query(models.SpeedRecord).offset(skip).limit(limit).all()


def create_speed_record(db: Session, record: schemas.SpeedRecordCreate, photo_url: str):
    """
    Creates a new groundspeed record. 
    The photo_url is provided after the file upload logic finishes.
    """
    db_record = models.SpeedRecord(
        pilot_name=record.pilot_name,
        groundspeed=record.groundspeed,
        description=record.description,
        model_id=record.model_id,
        photo_url=photo_url
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record