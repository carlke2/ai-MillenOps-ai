from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def classify(payload):
    return client.post("/v1/tickets/classify", json=payload)


def test_projector_ticket_returns_av_projector():
    response = classify({
        "ticketId": "ticket_001",
        "title": "Projector not working",
        "description": "The projector in Boardroom A is not displaying",
        "roomName": "Boardroom A",
        "bookingLinked": True,
        "department": "Operations"
    })

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["capability"] == "TICKET_CLASSIFICATION"
    assert data["recommendation"]["category"] == "AV / Projector"
    assert data["modelVersion"] == "baseline-rules-v1"


def test_network_ticket_returns_network():
    response = classify({
        "ticketId": "ticket_002",
        "title": "Wi-Fi is down",
        "description": "Internet is not working in the meeting room",
        "roomName": "Meeting Room 2",
        "bookingLinked": True,
        "department": "IT"
    })

    data = response.json()

    assert response.status_code == 200
    assert data["recommendation"]["category"] == "Network"


def test_hvac_ticket_returns_hvac():
    response = classify({
        "ticketId": "ticket_003",
        "title": "AC not cooling",
        "description": "The room is too hot and the air conditioner is not working",
        "roomName": "Boardroom B",
        "bookingLinked": False,
        "department": "Admin"
    })

    data = response.json()

    assert response.status_code == 200
    assert data["recommendation"]["category"] == "HVAC / Facility"


def test_unknown_ticket_returns_general_service():
    response = classify({
        "ticketId": "ticket_004",
        "title": "Need help",
        "description": "I need assistance with something",
        "roomName": "",
        "bookingLinked": False,
        "department": "Operations"
    })

    data = response.json()

    assert response.status_code == 200
    assert data["recommendation"]["category"] == "General Service"
