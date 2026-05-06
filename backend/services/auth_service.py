from importlib import import_module

try:
    _auth_service = import_module("backend.app.services.auth_service")
except ModuleNotFoundError:
    _auth_service = import_module("app.services.auth_service")

login_user = _auth_service.login_user
register_user = _auth_service.register_user

__all__ = ["login_user", "register_user"]
