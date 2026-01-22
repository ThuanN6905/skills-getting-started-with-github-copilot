import pytest
from fastapi.testclient import TestClient

import copy
from src.app import app, activities


# Save the original activities state for test isolation
original_activities = copy.deepcopy(activities)
client = TestClient(app)

import pytest

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset activities before each test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    if test_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(test_email)
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert test_email in activities[activity]["participants"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response2.status_code == 400
    # Unregister
    response3 = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response3.status_code == 200
    assert test_email not in activities[activity]["participants"]
    # Unregister again should fail
    response4 = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response4.status_code == 404

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    assert response.status_code == 404
