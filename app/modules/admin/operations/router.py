from fastapi import APIRouter
from app.modules.admin.operations.schemas import (
    AdminOperationsRequest,
    AdminOperationsResponse
)
from app.modules.admin.operations.service import analyze_operations

router = APIRouter(
    prefix="/admin",
    tags=["Admin Operations Intelligence"]
)

@router.post("/operations-analyze", response_model=AdminOperationsResponse)
def analyze_operations_endpoint(payload: AdminOperationsRequest):
    return analyze_operations(payload)
