from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from app.core.logger import logger

# Connect arguments (specific for SQLite during local mock testing)
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

try:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True
    )
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
except Exception as e:
    logger.warning(f"Failed to connect to DATABASE_URL ({settings.DATABASE_URL}). Falling back to local SQLite database: sqlite:///./test.db. Error: {e}")
    engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    FastAPI dependency to yield database sessions.
    Guarantees session cleanup after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import time
import threading

_db_status_cache = {"last_check": 0, "status": False}
_db_check_lock = threading.Lock()

def _bg_check_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        _db_status_cache["status"] = True
    except Exception:
        _db_status_cache["status"] = False

def check_db_connection() -> bool:
    """
    Executes a simple SELECT 1 query to test the database connection.
    Spawns a background thread to perform the check to prevent blocking API requests.
    """
    now = time.time()
    if now - _db_status_cache["last_check"] > 5.0:
        if _db_check_lock.acquire(blocking=False):
            try:
                _db_status_cache["last_check"] = now
                t = threading.Thread(target=_bg_check_db)
                t.daemon = True
                t.start()
            finally:
                _db_check_lock.release()
    return _db_status_cache["status"]
