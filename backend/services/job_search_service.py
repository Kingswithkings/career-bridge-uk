from importlib import import_module

try:
    _job_search_service = import_module("backend.app.services.job_search_service")
except ModuleNotFoundError:
    _job_search_service = import_module("app.services.job_search_service")

search_live_jobs = _job_search_service.search_live_jobs

__all__ = ["search_live_jobs"]
