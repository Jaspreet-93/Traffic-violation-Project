from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core import constants
from app.core.logger import logger
from app.database.connection import check_db_connection
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: test database connection
    logger.info("Starting up Smart Traffic Violation Detection API...")
    db_ok = check_db_connection()
    if db_ok:
        logger.info("Database connection test: SUCCESS")
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

# Register routers under version 1 prefix
app.include_router(api_router, prefix=constants.API_V1_STR)
