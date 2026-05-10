from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL as CONFIG_DATABASE_URL
from .config import IS_PRODUCTION

DATABASE_PATH = Path(__file__).resolve().parents[1] / "careerbridge.db"

if IS_PRODUCTION and not CONFIG_DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL must be set to a persistent database in production. "
        "The local SQLite fallback is only for development and will lose "
        "registered users on ephemeral hosts."
    )

DATABASE_URL = CONFIG_DATABASE_URL or f"sqlite:///{DATABASE_PATH}"

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
