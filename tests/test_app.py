import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
	# Arrange
	# (No special setup needed, just use the client)

	# Act
	response = client.get("/activities")

	# Assert
	assert response.status_code == 200
	data = response.json()
	assert isinstance(data, dict)
	assert "Chess Club" in data

def test_signup_for_activity_success():
	# Arrange
	activity = "Math Olympiad"
	email = "testuser1@mergington.edu"
	# Ensure user is not already signed up
	client.post(f"/activities/{activity}/unregister", params={"email": email})

	# Act
	response = client.post(f"/activities/{activity}/signup", params={"email": email})

	# Assert
	assert response.status_code == 200
	assert f"Signed up {email} for {activity}" in response.json()["message"]

def test_signup_for_activity_already_signed_up():
	# Arrange
	activity = "Chess Club"
	email = "michael@mergington.edu"  # Already signed up

	# Act
	response = client.post(f"/activities/{activity}/signup", params={"email": email})

	# Assert
	assert response.status_code == 400
	assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_for_nonexistent_activity():
	# Arrange
	activity = "Nonexistent Club"
	email = "someone@mergington.edu"

	# Act
	response = client.post(f"/activities/{activity}/signup", params={"email": email})

	# Assert
	assert response.status_code == 404
	assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_success():
	# Arrange
	activity = "Science Club"
	email = "testuser2@mergington.edu"
	# Ensure user is signed up
	client.post(f"/activities/{activity}/signup", params={"email": email})

	# Act
	response = client.post(f"/activities/{activity}/unregister", params={"email": email})

	# Assert
	assert response.status_code == 200
	assert f"Removed {email} from {activity}" in response.json()["message"]

def test_unregister_from_activity_not_found():
	# Arrange
	activity = "Art Club"
	email = "notregistered@mergington.edu"

	# Act
	response = client.post(f"/activities/{activity}/unregister", params={"email": email})

	# Assert
	assert response.status_code == 404
	assert response.json()["detail"] == "Participant not found in this activity"

def test_unregister_from_nonexistent_activity():
	# Arrange
	activity = "Nonexistent Club"
	email = "someone@mergington.edu"

	# Act
	response = client.post(f"/activities/{activity}/unregister", params={"email": email})

	# Assert
	assert response.status_code == 404
	assert response.json()["detail"] == "Activity not found"
