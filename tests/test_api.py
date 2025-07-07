import uuid
from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_appointment():
    # Test data
    start_time = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(
        days=1
    )
    appointment_data = {
        "patient_name": "John Doe",
        "doctor_id": 1,
        "start_time": start_time.isoformat(),
    }

    # Create appointment
    response = client.post("/appointments", json=appointment_data)
    assert response.status_code == 201
    created_appointment = response.json()

    # Get appointment
    appointment_id = created_appointment["id"]
    response = client.get(f"/appointments/{appointment_id}")
    assert response.status_code == 200
    assert response.json()["patient_name"] == "John Doe"

    # Test conflict
    response = client.post("/appointments", json=appointment_data)
    assert response.status_code == 409

    # Test not found
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/appointments/{non_existent_id}")
    assert response.status_code == 404
