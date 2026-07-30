import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_state():
    original_participants = {
        name: list(data["participants"])
        for name, data in app_module.activities.items()
    }
    yield
    for name, data in app_module.activities.items():
        data["participants"] = original_participants[name][:]


client = TestClient(app_module.app)


def test_unregister_participant():
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert signup_response.status_code == 200
    assert email in app_module.activities["Chess Club"]["participants"]

    unregister_response = client.delete(f"/activities/Chess Club/participants/{email}")
    assert unregister_response.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_unregister_nonexistent_participant():
    response = client.delete("/activities/Chess Club/participants/ghost@mergington.edu")
    assert response.status_code == 404
