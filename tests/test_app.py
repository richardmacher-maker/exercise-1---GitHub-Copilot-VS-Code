from fastapi.testclient import TestClient

from src import app as app_module


def setup_function():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    client = TestClient(app_module.app)
    activity_name = "Chess Club"
    student_email = "student@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={student_email}"
    )
    unregister_response = client.post(
        f"/activities/{activity_name}/unregister?email={student_email}"
    )
    activities_response = client.get("/activities")
    chess_club_activity = activities_response.json()[activity_name]
    updated_participants = chess_club_activity["participants"]

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert student_email not in updated_participants


def test_duplicate_signup_returns_bad_request():
    # Arrange
    client = TestClient(app_module.app)
    activity_name = "Chess Club"
    existing_student_email = "michael@mergington.edu"

    # Act
    duplicate_signup_response = client.post(
        f"/activities/{activity_name}/signup?email={existing_student_email}"
    )

    # Assert
    assert duplicate_signup_response.status_code == 400
    assert "already signed up" in duplicate_signup_response.json()["detail"].lower()
