"""Zoho Mail transport for the .com data centre, using HTTPS only."""

import logging
import threading
import time

import httpx

from .. import config

logger = logging.getLogger(__name__)
_token_lock = threading.Lock()
_access_token = None
_expires_at = 0.0


def is_selected() -> bool:
    return bool(config.ZOHO_CLIENT_ID)


def _get_access_token(client) -> str:
    global _access_token, _expires_at
    with _token_lock:
        if _access_token and time.monotonic() < _expires_at:
            return _access_token
        response = client.post(
            "https://accounts.zoho.com/oauth/v2/token",
            data={
                "grant_type": "refresh_token",
                "client_id": config.ZOHO_CLIENT_ID,
                "client_secret": config.ZOHO_CLIENT_SECRET,
                "refresh_token": config.ZOHO_REFRESH_TOKEN,
            },
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("error") or not payload.get("access_token"):
            raise ValueError("Zoho token refresh failed")
        lifetime = max(0, int(payload.get("expires_in", 3600)) - 60)
        _access_token = payload["access_token"]
        _expires_at = time.monotonic() + lifetime
        return _access_token


def send_message(message) -> bool:
    if not all((config.ZOHO_CLIENT_ID, config.ZOHO_CLIENT_SECRET,
                config.ZOHO_REFRESH_TOKEN, config.ZOHO_ACCOUNT_ID, config.ZOHO_FROM_EMAIL)):
        logger.error("Zoho email settings incomplete: client ID, secret, refresh token, account ID and sender are required")
        return False
    try:
        with httpx.Client(timeout=15.0) as client:
            token = _get_access_token(client)
            response = client.post(
                f"https://mail.zoho.com/api/accounts/{config.ZOHO_ACCOUNT_ID}/messages",
                headers={"Authorization": f"Zoho-oauthtoken {token}"},
                json={
                    "fromAddress": config.ZOHO_FROM_EMAIL,
                    "toAddress": str(message["To"]),
                    "subject": str(message["Subject"]),
                    "content": message.get_content(),
                    "mailFormat": "plaintext",
                    "encoding": "UTF-8",
                },
            )
            response.raise_for_status()
            if response.json().get("status", {}).get("code") != 200:
                raise ValueError("Zoho did not accept the email")
    except Exception as exc:
        # Provider responses can contain personal data or credentials. Log only type.
        logger.error("Zoho email delivery failed (%s)", type(exc).__name__)
        return False
    return True
