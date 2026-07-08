from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core import constants
from app.core.logger import logger
from app.database.connection import engine, check_db_connection
from app.database.base import Base
from app.api.v1.router import api_router
from app.api.v1.routes import system

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: test database connection
    logger.info("Starting up Smart Traffic Violation Detection API...")
    db_ok = check_db_connection()
    if db_ok:
        logger.info("Database connection test: SUCCESS")
        try:
            logger.info("Creating database tables if they do not exist...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables initialized successfully.")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
    else:
        logger.error("Database connection test: FAILED. Ensure database is running and credentials in .env are correct.")
    yield
    # Shutdown
    logger.info("Shutting down Smart Traffic Violation Detection API...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for logging and managing AI-detected traffic violations, vehicles, and administration dashboard logs.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register root level system router (GET / and GET /health)
app.include_router(system.router)

# Register routers under version 1 prefix
app.include_router(api_router, prefix=constants.API_V1_STR)

# Mount outputs folder statically to serve violation images/videos
from fastapi.staticfiles import StaticFiles
import os
outputs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))
os.makedirs(outputs_dir, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=outputs_dir), name="outputs")

# Mount uploads folder statically to serve uploaded snapshots/videos
uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
