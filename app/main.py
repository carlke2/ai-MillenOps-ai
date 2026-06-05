from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.security import get_api_key
from app.modules.tickets.classification.router import router as ticket_classification_router

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

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    }
