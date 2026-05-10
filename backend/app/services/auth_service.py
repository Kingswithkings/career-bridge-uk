from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.user_model import User
from ..utils.security import create_access_token, hash_password, verify_password


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_password(password: str) -> str:
    return password.strip()


def register_user(
    db: Session,
    email: str,
    password: str,
    full_name: str | None = None,
):
    email = normalize_email(email)
    password = normalize_password(password)

    if not password:
        raise HTTPException(status_code=400, detail="Password is required")

    existing_user = db.query(User).filter(func.lower(User.email) == email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        full_name=full_name.strip() if full_name else None,
        email=email,
        hashed_password=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": user.email,
    }


def login_user(db: Session, email: str, password: str):
    email = normalize_email(email)
    password = normalize_password(password)
    user = db.query(User).filter(func.lower(User.email) == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": user.email,
    }
