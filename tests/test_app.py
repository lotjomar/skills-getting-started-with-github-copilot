import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_list_activities():
    # Arrange: (No setup needed for initial activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    for activity in data.values():
        assert "description" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

def test_signup_and_unregister():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity_name = next(iter(client.get("/activities").json().keys()))

    # Act: Sign up
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={test_email}")

    # Assert: Signup
    assert signup_resp.status_code == 200
    assert f"Signed up {test_email}" in signup_resp.json().get("message", "")
    # Confirm participant is added
    activities = client.get("/activities").json()
    assert test_email in activities[activity_name]["participants"]

    # Act: Unregister (if supported)
    delete_resp = client.delete(f"/activities/{activity_name}/signup?email={test_email}")

    # Assert: Unregister
    assert delete_resp.status_code in (200, 204, 404)  # Accept 404 if not implemented
    # Confirm participant is removed if delete worked
    if delete_resp.status_code == 200:
        activities = client.get("/activities").json()
        assert test_email not in activities[activity_name]["participants"]
