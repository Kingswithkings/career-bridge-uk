from importlib import import_module

try:
    _security = import_module("backend.app.utils.security")
except ModuleNotFoundError:
    _security = import_module("app.utils.security")

create_access_token = _security.create_access_token
hash_password = _security.hash_password
verify_password = _security.verify_password

__all__ = ["create_access_token", "hash_password", "verify_password"]
