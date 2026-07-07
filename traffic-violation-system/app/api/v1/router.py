from fastapi import APIRouter
from app.api.v1.routes import system, camera, violation, violations, evidence, analytics, email_logs, camera_stream, detection, tracking, helmet, number_plate, ocr, seat_belt, traffic_light, driver_behavior

api_router = APIRouter()

# Include system and other routers under version 1
api_router.include_router(system.router)
api_router.include_router(camera_stream.router)
api_router.include_router(camera.router)
api_router.include_router(violation.router)
api_router.include_router(violations.router)
api_router.include_router(evidence.router)
api_router.include_router(analytics.router)
api_router.include_router(email_logs.router)
api_router.include_router(detection.router)
api_router.include_router(tracking.router)
api_router.include_router(helmet.router)
api_router.include_router(number_plate.router)
api_router.include_router(ocr.router)
api_router.include_router(seat_belt.router)
api_router.include_router(traffic_light.router)
api_router.include_router(driver_behavior.router)
