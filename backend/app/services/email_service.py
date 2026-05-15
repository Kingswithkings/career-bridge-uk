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
                "Welcome to CareerBridge UK. Your account has been created successfully.",
                "",
                "CareerBridge UK is built to help you organise your career journey, focus on the roles that matter most, and put your job priorities first.",
                "",
                "With CareerBridge UK, you can analyse your CV, match your experience to job opportunities, prepare for interviews, and keep your progress organised in one place.",
                "",
                f"Log in to your account here: {FRONTEND_URL}",
                "",
                "You can also visit our company website:",
                "https://1st-kings.com",
                "",
                "Thank you for choosing CareerBridge UK. We are pleased to support your next career move.",
                "",
                "Kind regards,",
                "The CareerBridge UK Team",
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
        logger.exception("Failed to send welcome email to %s", email)
        return False

    return True


def send_password_reset_code(
    email: str,
    code: str,
    full_name: str | None = None,
) -> bool:
    if not _smtp_is_configured():
        logger.info("Skipping password reset email because SMTP is not configured")
        return False

    display_name = full_name.strip() if full_name else "there"
    message = EmailMessage()
    message["Subject"] = "Reset your CareerBridge UK password"
    message["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    message["To"] = email
    message.set_content(
        "\n".join(
            [
                f"Hi {display_name},",
                "",
                "We received a request to reset the password for your CareerBridge UK account.",
                "",
                "Use this password reset code:",
                "",
                code,
                "",
                "This code expires in 15 minutes. If you did not request a password reset, you can safely ignore this email.",
                "",
                "You can visit our company website here:",
                "https://1st-kings.com",
                "",
                "Kind regards,",
                "The CareerBridge UK Team",
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
        logger.exception("Failed to send password reset email to %s", email)
        return False

    return True
