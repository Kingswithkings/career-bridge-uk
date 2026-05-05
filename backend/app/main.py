from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .api.routes.cv_routes import router as cv_router
from .api.routes.interview_routes import router as interview_router
from .api.routes.job_routes import router as job_router

app = FastAPI(
    title="CareerBridge UK API",
    description="Backend API for CV analysis and career support features.",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "CareerBridge UK API",
        "docs": "/docs",
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid request body. Check that your JSON is valid and required fields are present.",
            "errors": exc.errors(),
        },
    )


app.include_router(cv_router)
app.include_router(interview_router)
app.include_router(job_router)
