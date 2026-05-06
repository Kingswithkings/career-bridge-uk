from importlib import import_module

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .api.routes.auth_routes import router as auth_router
from .api.routes.cv_routes import router as cv_router
from .api.routes.interview_routes import router as interview_router
from .api.routes.job_routes import router as job_router
from .api.routes.result_routes import router as result_router
from .database import Base, engine

import_module(f"{__package__}.models.result_model")
import_module(f"{__package__}.models.user_model")
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CareerBridge UK API",
    description="AI-powered career mentor for UK job seekers.",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(cv_router)
app.include_router(interview_router)
app.include_router(job_router)
app.include_router(result_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": "Invalid request body. Check the required fields and JSON format.",
        },
    )


@app.get("/")
def root():
    return {
        "message": "CareerBridge UK Backend Running",
        "docs": "/docs",
    }
