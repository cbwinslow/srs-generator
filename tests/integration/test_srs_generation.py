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

def test_full_srs_generation_flow(client, mocker):
    """Test the complete flow of SRS generation."""
    # Mock the AI response
    mock_sections = {
        "introduction": "# Introduction\nThis is a test introduction.",
        "functional_requirements": "# Functional Requirements\n- Requirement 1\n- Requirement 2",
        "non_functional_requirements": "# Non-Functional Requirements\n1. Performance\n2. Security",
        "constraints": "# Constraints\n* Technical constraints\n* Business constraints"
    }
    
    mock_generator = mocker.patch("backend.ai.routes.AIGenerator")
    mock_generator.return_value.generate_srs.return_value = mock_sections
    
    # Test data
    test_data = {
        "projectName": "Test Project",
        "targetUsers": "Test Users",
        "projectGoals": "Create a test project",
        "projectScope": "Testing scope"
    }
    
    # Make request
    response = client.post("/api/v1/generate_srs",
                         json=test_data,
                         headers={"Content-Type": "application/json"})
    
    # Verify response
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "sections" in data
    
    # Verify sections
    sections = data["sections"]
    assert all(key in sections for key in ["introduction", "functional_requirements", 
                                         "non_functional_requirements", "constraints"])
    assert all(isinstance(sections[key], str) for key in sections)
    
    # Verify mock was called correctly
    mock_generator.return_value.generate_srs.assert_called_once_with(test_data)

def test_error_handling_with_invalid_api_key(client):
    """Test error handling when API key is invalid."""
    test_data = {
        "projectName": "Test Project",
        "targetUsers": "Test Users",
        "projectGoals": "Create a test project",
        "projectScope": "Testing scope"
    }
    
    # Configure app with invalid API key
    client.application.config["OPENROUTER_API_KEY"] = "invalid-key"
    
    response = client.post("/api/v1/generate_srs",
                         json=test_data,
                         headers={"Content-Type": "application/json"})
    
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data
    assert "details" in data
