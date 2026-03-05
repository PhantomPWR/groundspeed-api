"""
Authentication endpoints for user registration and login.
"""

from datetime import timedelta                     # Standard: Time utilities
from fastapi import (                              # Third Party: Web tools
    APIRouter, Depends, HTTPException, status
)
from fastapi.security import (                     # Third Party: Auth
    OAuth2PasswordRequestForm
)
from sqlalchemy.orm import Session                 # Third Party: DB session
from app import crud, schemas, models, auth_utils  # Local: App modules
from app.database import get_db                    # Local: DB helper

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new public user with the 'user' role.
    """
    # 1. Check if email exists
    existing = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash password and save
    hashed_pwd = auth_utils.hash_password(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_pwd,
        full_name=user.full_name,
        role="user"  # Default role for all registrations
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Standard OAuth2 login flow. Returns a JWT access token.
    """
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not user or not auth_utils.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate the JWT
    access_token_expires = timedelta(
        minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = auth_utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
