from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@example.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200

    assert unregister_response.status_code == 200
    payload = unregister_response.json()
    assert payload["message"] == f"Removed {email} from {activity_name}"

    assert activities_response.status_code == 200
    activity = activities_response.json()[activity_name]
    assert email not in activity["participants"]
