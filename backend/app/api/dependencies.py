import base64
import hashlib
import hmac
import json
import time

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ..config import SECRET_KEY
from ..database import get_db
from ..models.user_model import User

security = HTTPBearer()


def _base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}")


def _decode_access_token(token: str) -> dict:
    try:
        header_part, payload_part, signature_part = token.split(".")
        signing_input = f"{header_part}.{payload_part}"
        expected_signature = hmac.new(
            SECRET_KEY.encode("utf-8"),
            signing_input.encode("ascii"),
            hashlib.sha256,
        ).digest()
        actual_signature = _base64url_decode(signature_part)

        if not hmac.compare_digest(actual_signature, expected_signature):
            raise ValueError("Invalid token signature")

        payload = json.loads(_base64url_decode(payload_part).decode("utf-8"))
        expires_at = payload.get("exp")

        if expires_at is not None and int(expires_at) < int(time.time()):
            raise ValueError("Expired token")

        return payload
    except (ValueError, TypeError, json.JSONDecodeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    payload = _decode_access_token(token)
    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
