from importlib import import_module

try:
    _job_search_schema = import_module("backend.app.schemas.job_search_schema")
except ModuleNotFoundError:
    _job_search_schema = import_module("app.schemas.job_search_schema")

JobSearchRequest = _job_search_schema.JobSearchRequest
JobItem = _job_search_schema.JobItem
JobSearchResponse = _job_search_schema.JobSearchResponse

__all__ = ["JobSearchRequest", "JobItem", "JobSearchResponse"]
