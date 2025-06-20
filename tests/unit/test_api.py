import pytest
from backend.app import create_app
from backend.config import TestingConfig


class TestConfig(TestingConfig):
    TESTING = True
    OPENROUTER_API_KEY = "test-key-for-testing"


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestConfig)
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_generate_srs_endpoint_exists(client):
    """Test that the generate_srs endpoint exists and returns 400 when no data is provided."""
    response = client.post(
        "/api/v1/generate_srs", headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "missing_fields" in data


def test_generate_srs_requires_data(client):
    """Test that the generate_srs endpoint requires specific fields."""
    response = client.post(
        "/api/v1/generate_srs", json={}, headers={"Content-Type": "application/json"}
    )
    data = response.get_json()
    assert response.status_code == 400
    assert "error" in data
    assert "missing_fields" in data
    assert len(data["missing_fields"]) == 4


def test_generate_srs_with_valid_data(client, mocker):
    """Test that the generate_srs endpoint works with valid data."""
    # Mock the AIGenerator class
    mock_sections = {
        "introduction": "Test introduction",
        "functional_requirements": "Test functional requirements",
        "non_functional_requirements": "Test non-functional requirements",
        "constraints": "Test constraints",
    }

    mock_generator = mocker.patch("backend.ai.routes.AIGenerator")
    mock_generator.return_value.generate_srs.return_value = mock_sections

    test_data = {
        "projectName": "Test Project",
        "targetUsers": "Test Users",
        "projectGoals": "Test Goals",
        "projectScope": "Test Scope",
    }

    response = client.post(
        "/api/v1/generate_srs",
        json=test_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "sections" in data
    assert data["sections"] == mock_sections
