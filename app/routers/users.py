"""
Administrative endpoints for managing system users.
"""

from typing import List                          # Standard: Type hinting
from fastapi import APIRouter, Depends           # Third Party: Web tools
from sqlalchemy.orm import Session               # Third Party: DB session
from app import crud, schemas, models            # Local: App modules
from app.database import get_db                  # Local: DB helper
from app.dependencies import (                   # Local: Auth guards
    get_current_active_owner
)

router = APIRouter(
    prefix="/users",
    tags=["User Management"]
)


@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _current_user: models.User = Depends(get_current_active_owner)
):
    """
    Returns a list of all users. Restricted to Owner only.
    """
    return crud.get_users(db, skip=skip, limit=limit)