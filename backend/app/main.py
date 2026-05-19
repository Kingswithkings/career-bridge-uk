from contextlib import asynccontextmanager
from importlib import import_module

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import inspect, text

from .api.routes.auth_routes import router as auth_router
from .api.routes.cv_routes import router as cv_router
from .api.routes.feedback_routes import router as feedback_router
from .api.routes.interview_routes import router as interview_router
from .api.routes.job_routes import router as job_router
from .api.routes.result_routes import router as result_router
from .database import Base, engine
from .limiter import limiter
from .posthog_client import posthog_client

import_module(f"{__package__}.models.result_model")
import_module(f"{__package__}.models.user_model")
import_module(f"{__package__}.models.feedback_model")
Base.metadata.create_all(bind=engine)


def ensure_user_verification_columns() -> None:
    inspector = inspect(engine)

    if "users" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("users")}
    dialect = engine.dialect.name

    statements = []
    if "is_email_verified" not in existing_columns:
        if dialect == "postgresql":
            statements.append(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_email_verified BOOLEAN NOT NULL DEFAULT FALSE"
            )
        else:
            statements.append(
                "ALTER TABLE users ADD COLUMN is_email_verified BOOLEAN NOT NULL DEFAULT 0"
            )

    if "email_verification_code_hash" not in existing_columns:
        if dialect == "postgresql":
            statements.append(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verification_code_hash VARCHAR"
            )
        else:
            statements.append("ALTER TABLE users ADD COLUMN email_verification_code_hash VARCHAR")

    if "email_verification_expires_at" not in existing_columns:
        if dialect == "postgresql":
            statements.append(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verification_expires_at TIMESTAMP"
            )
        else:
            statements.append("ALTER TABLE users ADD COLUMN email_verification_expires_at DATETIME")

    if "password_reset_code_hash" not in existing_columns:
        if dialect == "postgresql":
            statements.append(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_reset_code_hash VARCHAR"
            )
        else:
            statements.append("ALTER TABLE users ADD COLUMN password_reset_code_hash VARCHAR")

    if "password_reset_expires_at" not in existing_columns:
        if dialect == "postgresql":
            statements.append(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_reset_expires_at TIMESTAMP"
            )
        else:
            statements.append("ALTER TABLE users ADD COLUMN password_reset_expires_at DATETIME")

    if not statements:
        return

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


ensure_user_verification_columns()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    posthog_client.flush()


app = FastAPI(
    title="CareerBridge UK API",
    description="AI-powered career mentor for UK job seekers.",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://career-bridge-uk.1st-kings.com",
        "https://career-bridge-uk.vercel.app",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(cv_router)
app.include_router(interview_router)
app.include_router(job_router)
app.include_router(result_router)
app.include_router(feedback_router)


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


@app.get("/health")
def health_check():
    return {"status": "ok"}
