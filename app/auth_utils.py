"""
Utility functions for hashing passwords and managing JWT tokens.
"""

from datetime import datetime, timedelta, timezone  # Standard: Date/Time
from typing import Optional                         # Standard: Type hinting
from jose import jwt                                # Third Party: JWT logic
import bcrypt                                       # Third Party: Hashing

# Configuration (In production, move these to .env)
SECRET_KEY = "DEVELOPMENT_SECRET_KEY_CHANGE_THIS" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.
    """
    # Convert string to bytes
    pwd_bytes = password.encode('utf-8')
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Return as string for DB storage
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if a plain-text password matches a stored hash.
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Generates a JWT token containing user data.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
