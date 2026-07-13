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
        from app.utils.deletion_registry import load_deleted_ids
        import os
        import json
        
        evidence_fallback_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "fallback_evidence.json"))
        deleted_evidence = load_deleted_ids("evidence")
        if deleted_evidence and os.path.exists(evidence_fallback_path):
            try:
                with open(evidence_fallback_path, "r") as f:
                    data = json.load(f)
                filtered = [item for item in data if item.get("evidence_id") not in deleted_evidence]
                with open(evidence_fallback_path, "w") as f:
                    json.dump(filtered, f, indent=2)
                logger.info(f"Startup cleanup: Purged {len(data) - len(filtered)} deleted evidence records from fallback JSON.")
            except Exception as e:
                logger.error(f"Error purging fallback_evidence.json on startup: {e}")

        cameras_fallback_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "cameras.json"))
        deleted_cameras = load_deleted_ids("cameras")
        if deleted_cameras and os.path.exists(cameras_fallback_path):
            try:
                with open(cameras_fallback_path, "r") as f:
                    data = json.load(f)
                filtered = [item for item in data if item.get("id") not in deleted_cameras]
                with open(cameras_fallback_path, "w") as f:
                    json.dump(filtered, f, indent=2)
                logger.info(f"Startup cleanup: Purged {len(data) - len(filtered)} deleted camera records from fallback JSON.")
            except Exception as e:
                logger.error(f"Error purging cameras.json on startup: {e}")

        reports_fallback_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "reports.json"))
        deleted_reports = load_deleted_ids("reports")
        if deleted_reports and os.path.exists(reports_fallback_path):
            try:
                with open(reports_fallback_path, "r") as f:
                    data = json.load(f)
                filtered = [item for item in data if item.get("id") not in deleted_reports]
                with open(reports_fallback_path, "w") as f:
                    json.dump(filtered, f, indent=2)
                logger.info(f"Startup cleanup: Purged {len(data) - len(filtered)} deleted report records from fallback JSON.")
            except Exception as e:
                logger.error(f"Error purging reports.json on startup: {e}")

        uploads_fallback_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "upload_history.json"))
        deleted_uploads = load_deleted_ids("uploads")
        if deleted_uploads and os.path.exists(uploads_fallback_path):
            try:
                with open(uploads_fallback_path, "r") as f:
                    data = json.load(f)
                filtered = [item for item in data if item.get("job_id") not in deleted_uploads]
                with open(uploads_fallback_path, "w") as f:
                    json.dump(filtered, f, indent=2)
                logger.info(f"Startup cleanup: Purged {len(data) - len(filtered)} deleted upload history records from fallback JSON.")
            except Exception as e:
                logger.error(f"Error purging upload_history.json on startup: {e}")
    except Exception as e:
        logger.error(f"Error executing startup deletion cleanup: {e}")
    
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
from app.api.v1.routes.mobile_phone import router as mobile_phone_router
from app.api.v1.routes.red_light import router as red_light_router
from app.api.v1.routes.wrong_lane import router as wrong_lane_router
from app.api.v1.routes.rules import router as rules_router
from app.api.v1.routes.accuracy import router as accuracy_router
app.include_router(verification_router, prefix="/api")
app.include_router(seatbelt_router, prefix="/api")
app.include_router(mobile_phone_router, prefix="/api")
app.include_router(red_light_router, prefix="/api")
app.include_router(wrong_lane_router, prefix="/api")
app.include_router(rules_router, prefix="/api")
app.include_router(accuracy_router, prefix="/api")

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
