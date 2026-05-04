from fastapi import FastAPI

from app.api.routes.cv_routes import router as cv_router

app = FastAPI(
    title="CareerBridge UK API",
    description="Backend API for CV analysis and career support features.",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "CareerBridge UK API"}


app.include_router(cv_router)
