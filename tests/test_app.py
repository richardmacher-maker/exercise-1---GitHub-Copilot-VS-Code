from fastapi.testclient import TestClient

from src import app as app_module


def setup_function():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app_module.app)

    signup_response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )
    assert signup_response.status_code == 200

    unregister_response = client.post(
        "/activities/Chess Club/unregister?email=student@mergington.edu"
    )
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert "student@mergington.edu" not in participants
