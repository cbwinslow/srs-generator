import pytest
from backend.app import create_app
from backend.config import TestingConfig

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestingConfig)
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_generate_srs_endpoint_exists(client):
    """Test that the generate_srs endpoint exists and returns 400 when no data is provided."""
    response = client.post("/api/v1/generate_srs")
    assert response.status_code == 400

def test_generate_srs_requires_data(client):
    """Test that the generate_srs endpoint requires specific fields."""
    response = client.post("/api/v1/generate_srs", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "missing_fields" in data
    assert len(data["missing_fields"]) == 4  # All required fields should be missing

def test_generate_srs_with_valid_data(client):
    """Test that the generate_srs endpoint works with valid data."""
    test_data = {
        "projectName": "Test Project",
        "targetUsers": "Test Users",
        "projectGoals": "Test Goals",
        "projectScope": "Test Scope"
    }
    response = client.post("/api/v1/generate_srs", json=test_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
