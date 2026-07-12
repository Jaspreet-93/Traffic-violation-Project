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
    
    try:
        from app.services.upload_detection.upload_service import UploadService
        UploadService.resolve_pending_jobs()
    except Exception as e:
        logger.error(f"Error resolving pending upload jobs: {e}")
        
    db_ok = check_db_connection()
    if db_ok:
        logger.info("Database connection test: SUCCESS")
        try:
            logger.info("Creating database tables if they do not exist...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables initialized successfully.")
            
            # Ensure new columns exist in database table violations
            from sqlalchemy import text
            with engine.connect() as conn:
                for col in ["original_image", "annotated_image", "vehicle_crop", "helmet_crop", "seatbelt_crop", "plate_crop", "trafficlight_crop", "mobile_crop", "lane_crop"]:
                    try:
                        conn.execute(text(f"ALTER TABLE violations ADD COLUMN {col} VARCHAR"))
                        # Commit transaction for SQLite/Postgres
                        try:
                            conn.commit()
                        except Exception:
                            pass
                    except Exception:
                        pass
        except Exception as e:
            logger.error(f"Error creating/altering database tables: {e}")
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

# Register violations router directly under /api prefix for compatibility
from app.api.v1.routes.violations import router as violations_router
app.include_router(violations_router, prefix="/api")

# Register license-plates router under /api prefix
from app.api.v1.routes.license_plates import router as license_plates_router
app.include_router(license_plates_router, prefix="/api")

# Register AI Verification and Seatbelt routers
from app.api.v1.routes.verification import router as verification_router
from app.api.v1.routes.seatbelt import router as seatbelt_router
app.include_router(verification_router, prefix="/api")
app.include_router(seatbelt_router, prefix="/api")

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

# Mount storage folder statically to serve real validation crops
storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage"))
os.makedirs(storage_dir, exist_ok=True)
for sub in ["evidence", "original", "annotated", "vehicle", "helmet", "seatbelt", "plate", "trafficlight", "mobile", "lane"]:
    os.makedirs(os.path.join(storage_dir, sub), exist_ok=True)
app.mount("/storage", StaticFiles(directory=storage_dir), name="storage")
