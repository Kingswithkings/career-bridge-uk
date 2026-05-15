import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.user_model import User
from ..utils.security import create_access_token, hash_password, verify_password


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_password(password: str) -> str:
    return password.strip()


def generate_password_reset_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_password_reset_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


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


def create_password_reset_code(db: Session, email: str):
    email = normalize_email(email)
    user = db.query(User).filter(func.lower(User.email) == email).first()

    if not user:
        return None

    code = generate_password_reset_code()
    user.password_reset_code_hash = hash_password_reset_code(code)
    user.password_reset_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    db.commit()
    db.refresh(user)

    return {
        "email": user.email,
        "full_name": user.full_name,
        "code": code,
    }


def reset_user_password(db: Session, email: str, code: str, new_password: str):
    email = normalize_email(email)
    code = code.strip()
    new_password = normalize_password(new_password)

    if not new_password:
        raise HTTPException(status_code=400, detail="New password is required")

    user = db.query(User).filter(func.lower(User.email) == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset code")

    if not user.password_reset_code_hash or not user.password_reset_expires_at:
        raise HTTPException(status_code=400, detail="Invalid or expired reset code")

    expires_at = user.password_reset_expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired reset code")

    if hash_password_reset_code(code) != user.password_reset_code_hash:
        raise HTTPException(status_code=400, detail="Invalid or expired reset code")

    user.hashed_password = hash_password(new_password)
    user.password_reset_code_hash = None
    user.password_reset_expires_at = None
    db.commit()

    return {"message": "Password reset successfully"}


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
