from importlib import import_module

try:
    _user_model = import_module("backend.app.models.user_model")
except ModuleNotFoundError:
    _user_model = import_module("app.models.user_model")

User = _user_model.User

__all__ = ["User"]
