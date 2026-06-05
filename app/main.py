from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.security import get_api_key
from app.modules.tickets.classification.router import router as ticket_classification_router
from app.modules.tickets.priority.router import router as ticket_priority_router
from app.modules.tickets.routing.router import router as ticket_routing_router
from app.modules.rooms.recommendation.router import router as room_recommendation_router
from app.modules.nlp.assistant.router import router as meeting_assistant_router
from app.modules.visitors.reception.router import router as visitor_reception_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# Main API Router with global security and /v1 prefix
app.include_router(
    ticket_classification_router,
    prefix="/v1",
    dependencies=[Depends(get_api_key)]
)

app.include_router(
    ticket_priority_router,
    prefix="/v1",
    dependencies=[Depends(get_api_key)]
)

app.include_router(
    ticket_routing_router,
    prefix="/v1",
    dependencies=[Depends(get_api_key)]
)

app.include_router(
    room_recommendation_router,
    prefix="/v1",
    dependencies=[Depends(get_api_key)]
)

app.include_router(
    meeting_assistant_router,
    prefix="/v1",
    dependencies=[Depends(get_api_key)]
)

app.include_router(
    visitor_reception_router,
    prefix="/v1",
    dependencies=[Depends(get_api_key)]
)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    }
