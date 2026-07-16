import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client


def test_get_activities_returns_expected_activity_data(client):
    # Arrange
    expected_activity_name = "Chess Club"
    expected_max_participants = 12
    expected_participant = "michael@mergington.edu"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity_name in payload
    assert payload[expected_activity_name]["max_participants"] == expected_max_participants
    assert expected_participant in payload[expected_activity_name]["participants"]


def test_signup_and_unregister_flow(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@example.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_duplicate_signup_returns_bad_request(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"
