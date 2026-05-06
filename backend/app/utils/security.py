import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone

from ..config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY

PASSWORD_ALGORITHM = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 100_000


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _json_base64url(data: dict) -> str:
    return _base64url_encode(
        json.dumps(data, separators=(",", ":"), default=str).encode("utf-8")
    )


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        PASSWORD_ITERATIONS,
    ).hex()
    return f"{PASSWORD_ALGORITHM}${PASSWORD_ITERATIONS}${salt}${digest}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algorithm, iterations, salt, expected_digest = hashed_password.split("$", 3)
        if algorithm != PASSWORD_ALGORITHM:
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            bytes.fromhex(salt),
            int(iterations),
        ).hex()
    except (ValueError, TypeError):
        return False

    return hmac.compare_digest(digest, expected_digest)


def create_access_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    payload["exp"] = int(expire.timestamp())

    signing_input = f"{_json_base64url(header)}.{_json_base64url(payload)}"
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        signing_input.encode("ascii"),
        hashlib.sha256,
    ).digest()

    return f"{signing_input}.{_base64url_encode(signature)}"
