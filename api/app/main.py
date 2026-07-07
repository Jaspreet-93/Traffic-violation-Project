from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import check_db_connection
from app.routers import system
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: test database connection
    logger.info("Starting up Traffic Violation Detection API...")
    db_ok = check_db_connection()
    if db_ok:
        logger.info("Database connection test: SUCCESS")
    else:
        logger.error("Database connection test: FAILED. Ensure database is running and credentials in .env are correct.")
    yield
    # Shutdown
    logger.info("Shutting down Traffic Violation Detection API...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for logging and managing AI-detected traffic violations, vehicles, and administration dashboard logs.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(system.router)
