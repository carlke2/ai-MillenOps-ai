import logging
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.security import get_api_key

# Import all routers
from app.modules.tickets.classification.router import router as ticket_classification_router
from app.modules.tickets.priority.router import router as ticket_priority_router
from app.modules.tickets.routing.router import router as ticket_routing_router
from app.modules.rooms.recommendation.router import router as room_recommendation_router
from app.modules.nlp.assistant.router import router as meeting_assistant_router
from app.modules.visitors.reception.router import router as visitor_reception_router
from app.modules.visitors.matching.router import router as visitor_matching_router
from app.modules.meetings.reminders.router import router as meeting_reminder_router
from app.modules.bookings.no_show.router import router as booking_no_show_router
from app.modules.rooms.release.router import router as room_release_router
from app.modules.admin.operations.router import router as admin_operations_router
from app.modules.nlp.chatbot.router import router as chatbot_router
from app.modules.anomalies.detection.router import router as anomaly_detection_router
from app.modules.workforce.insight.router import router as workforce_insight_router
from app.modules.facilities.forecasting.router import router as facility_forecasting_router

# Structured Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("smart-ops-ai")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# Configuration-driven router registration
ROUTERS = [
    ticket_classification_router,
    ticket_priority_router,
    ticket_routing_router,
    room_recommendation_router,
    meeting_assistant_router,
    visitor_reception_router,
    visitor_matching_router,
    meeting_reminder_router,
    booking_no_show_router,
    room_release_router,
    admin_operations_router,
    chatbot_router,
    anomaly_detection_router,
    workforce_insight_router,
    facility_forecasting_router
]

for router in ROUTERS:
    app.include_router(
        router,
        prefix="/v1",
        dependencies=[Depends(get_api_key)]
    )

# Global Error Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": str(exc) if settings.APP_ENV == "development" else "An unexpected error occurred."
        }
    )

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    }
