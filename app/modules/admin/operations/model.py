from app.modules.admin.operations.schemas import AdminOperationsRequest
from app.modules.admin.operations.rules import analyze_operations_with_rules

def analyze_operations_with_model(payload: AdminOperationsRequest):
    return analyze_operations_with_rules(payload)
