from importlib import import_module

try:
    _email_service = import_module("backend.app.services.email_service")
except ModuleNotFoundError:
    _email_service = import_module("app.services.email_service")

send_registration_confirmation_email = (
    _email_service.send_registration_confirmation_email
)

__all__ = ["send_registration_confirmation_email"]
