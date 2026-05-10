import logging
import smtplib
from email.message import EmailMessage

from ..config import (
    FRONTEND_URL,
    SMTP_FROM_EMAIL,
    SMTP_FROM_NAME,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_USE_TLS,
)

logger = logging.getLogger(__name__)


def _smtp_is_configured() -> bool:
    return bool(SMTP_HOST and SMTP_FROM_EMAIL)


def send_registration_confirmation_email(
    email: str,
    full_name: str | None = None,
) -> bool:
    if not _smtp_is_configured():
        logger.info("Skipping registration email because SMTP is not configured")
        return False

    display_name = full_name.strip() if full_name else "there"
    message = EmailMessage()
    message["Subject"] = "Welcome to CareerBridge UK"
    message["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    message["To"] = email
    message.set_content(
        "\n".join(
            [
                f"Hi {display_name},",
                "",
                "Your CareerBridge UK account has been created successfully.",
                "",
                f"You can log in here: {FRONTEND_URL}",
                "",
                "CareerBridge UK",
            ]
        )
    )

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            if SMTP_USE_TLS:
                server.starttls()
            if SMTP_USERNAME and SMTP_PASSWORD:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
    except Exception:
        logger.exception("Failed to send registration confirmation email to %s", email)
        return False

    return True
