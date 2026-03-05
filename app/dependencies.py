"""
Dependencies for enforcing user authentication and role-based access.
"""

from fastapi import Depends, HTTPException, status  # Third Party: Web tools
from fastapi.security import OAuth2PasswordBearer   # Third Party: Auth
from jose import JWTError, jwt                      # Third Party: JWT
from sqlalchemy.orm import Session                  # Third Party: DB session
from app import models, auth_utils                  # Local: App modules
from app.database import get_db                     # Local: DB helper

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Validates the JWT token and returns the current user object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, auth_utils.SECRET_KEY, algorithms=[auth_utils.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_admin(user: models.User = Depends(get_current_user)):
    """
    Enforces that the user must be an Admin or Owner.
    """
    if user.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions (Admin/Owner only)"
        )
    return user


def get_current_active_owner(user: models.User = Depends(get_current_user)):
    """
    Enforces that the user must be the Owner.
    """
    if user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions (Owner only)"
        )
    return user
