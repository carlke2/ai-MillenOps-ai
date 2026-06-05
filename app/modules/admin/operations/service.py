from app.modules.admin.operations.schemas import AdminOperationsRequest
from app.modules.admin.operations.model import analyze_operations_with_model

def analyze_operations(payload: AdminOperationsRequest):
    return analyze_operations_with_model(payload)
