"""
Create, Read, Update, and Delete logic for the database.
"""

from sqlalchemy.orm import Session       # Third Party: DB session tool
from app import models, schemas          # Local: DB models and schemas


# --- CATEGORY CRUD ---

def get_categories(db: Session):
    """
    Fetches all aircraft categories from the database.
    """
    return db.query(models.Category).all()


def get_category(db: Session, category_id: int):
    """
    Fetches a single category by its ID.
    """
    return db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()


def create_category(db: Session, category: schemas.CategoryCreate):
    """
    Creates a new aircraft category.
    """
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
    db: Session,
    category_id: int,
    category_update: schemas.CategoryUpdate
):
    """
    Updates an existing category.
    """
    db_category = get_category(db, category_id)
    if db_category:
        update_data = category_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    """
    Deletes a category from the database.
    """
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


# --- MANUFACTURER CRUD ---

def get_manufacturers(db: Session, category_id: int = None):
    """
    Fetches manufacturers, optionally filtered by category.
    """
    query = db.query(models.Manufacturer)
    if category_id:
        query = query.filter(models.Manufacturer.category_id == category_id)
    return query.all()


def get_manufacturer(db: Session, manufacturer_id: int):
    """
    Fetches a single manufacturer by its ID.
    """
    return db.query(models.Manufacturer).filter(
        models.Manufacturer.id == manufacturer_id
    ).first()


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


def update_manufacturer(
    db: Session,
    manufacturer_id: int,
    manufacturer_update: schemas.ManufacturerUpdate
):
    """
    Updates an existing manufacturer's details.
    """
    db_man = get_manufacturer(db, manufacturer_id)
    if db_man:
        update_data = manufacturer_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_man, key, value)
        db.commit()
        db.refresh(db_man)
    return db_man


def delete_manufacturer(db: Session, manufacturer_id: int):
    """
    Deletes a manufacturer from the database.
    """
    db_man = get_manufacturer(db, manufacturer_id)
    if db_man:
        db.delete(db_man)
        db.commit()
        return True
    return False


# --- AIRCRAFT MODEL CRUD ---

def get_aircraft_models(db: Session, manufacturer_id: int = None):
    """
    Fetches aircraft models, optionally filtered by manufacturer.
    """
    query = db.query(models.AircraftModel)
    if manufacturer_id:
        query = query.filter(
            models.AircraftModel.manufacturer_id == manufacturer_id
        )
    return query.all()


def get_aircraft_model(db: Session, aircraft_model_id: int):
    """
    Fetches a single aircraft model by its ID.
    """
    return db.query(models.AircraftModel).filter(
        models.AircraftModel.id == aircraft_model_id
    ).first()


def create_aircraft_model(
    db: Session,
    aircraft_model: schemas.AircraftModelCreate,
    image_url: str = None
):
    """
    Creates a new aircraft model with technical specifications.
    """
    db_model = models.AircraftModel(
        name=aircraft_model.name,
        image_url=image_url,
        passengers=aircraft_model.passengers,
        max_takeoff_weight=aircraft_model.max_takeoff_weight,
        max_landing_weight=aircraft_model.max_landing_weight,
        max_fuel_capacity=aircraft_model.max_fuel_capacity,
        max_range=aircraft_model.max_range,
        max_ceiling=aircraft_model.max_ceiling,
        max_cruising_speed=aircraft_model.max_cruising_speed,
        thrust_power=aircraft_model.thrust_power,
        manufacturer_id=aircraft_model.manufacturer_id
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def update_aircraft_model(
    db: Session,
    aircraft_model_id: int,
    model_update: schemas.AircraftModelUpdate,
    image_url: str = None
):
    """
    Updates an existing aircraft model's specs and optional image.
    """
    db_model = get_aircraft_model(db, aircraft_model_id)
    if db_model:
        update_data = model_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_model, key, value)
        if image_url:
            db_model.image_url = image_url
        db.commit()
        db.refresh(db_model)
    return db_model


def delete_aircraft_model(db: Session, aircraft_model_id: int):
    """
    Deletes an aircraft model from the database.
    """
    db_model = get_aircraft_model(db, aircraft_model_id)
    if db_model:
        db.delete(db_model)
        db.commit()
        return True
    return False


# --- SPEED RECORD CRUD ---

def get_records(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches groundspeed records with pagination.
    """
    return db.query(models.SpeedRecord).offset(skip).limit(limit).all()


def create_speed_record(
    db: Session,
    record: schemas.SpeedRecordCreate,
    photo_url: str
):
    """
    Creates a new groundspeed record linked to an aircraft model.
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
