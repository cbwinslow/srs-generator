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


def test_start_interactive_session(client, mocker):
    """Test starting a new interactive session."""
    # Mock the InteractiveAgent
    mock_agent_class = mocker.patch("backend.ai.routes.InteractiveAgent")
    mock_agent = mock_agent_class.return_value

    mock_agent.start_conversation.return_value = {
        "message": "Hello! Let's start creating your SRS.",
        "conversation_id": 12345,
        "progress": {
            "percentage": 0,
            "completed_sections": [],
            "missing_sections": ["project_overview"],
            "total_sections": 5,
        },
        "next_steps": ["project_overview"],
    }

    # Make request
    response = client.post("/api/v1/interactive/start")

    # Verify response
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "session_id" in data
    assert "message" in data
    assert data["message"] == "Hello! Let's start creating your SRS."
    assert "progress" in data
    assert data["progress"]["percentage"] == 0


def test_respond_to_agent(client, mocker):
    """Test sending a response to the interactive agent."""
    # First start a session
    mock_agent_class = mocker.patch("backend.ai.routes.InteractiveAgent")
    mock_agent = mock_agent_class.return_value

    mock_agent.start_conversation.return_value = {
        "message": "Hello! Let's start.",
        "conversation_id": 12345,
        "progress": {"percentage": 0},
        "next_steps": [],
    }

    start_response = client.post("/api/v1/interactive/start")
    session_id = start_response.get_json()["session_id"]

    # Mock the process_user_input method
    mock_agent.process_user_input.return_value = {
        "message": "Great! What are the main features?",
        "collected_data": {"raw_notes": ["My project is a mobile app"]},
        "progress": {"percentage": 20},
        "complete": False,
    }

    # Send a message
    response = client.post(
        "/api/v1/interactive/respond",
        json={"session_id": session_id, "message": "My project is a mobile app"},
    )

    # Verify response
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "in_progress"
    assert "message" in data
    assert "progress" in data


def test_respond_to_agent_complete(client, mocker):
    """Test completing an interactive session."""
    # Start session
    mock_agent_class = mocker.patch("backend.ai.routes.InteractiveAgent")
    mock_agent = mock_agent_class.return_value

    mock_agent.start_conversation.return_value = {
        "message": "Hello!",
        "conversation_id": 12345,
        "progress": {"percentage": 0},
        "next_steps": [],
    }

    start_response = client.post("/api/v1/interactive/start")
    session_id = start_response.get_json()["session_id"]

    # Mock completion response
    mock_agent.process_user_input.return_value = {
        "message": "Great! Generating document...",
        "collected_data": {"raw_notes": ["Complete project info"]},
        "progress": {"percentage": 100},
        "complete": True,
    }

    mock_sections = {
        "introduction": "# Introduction content",
        "functional_requirements": "# FR content",
        "non_functional_requirements": "# NFR content",
        "constraints": "# Constraints content",
    }
    mock_agent.generate_complete_srs.return_value = mock_sections

    # Send final message
    response = client.post(
        "/api/v1/interactive/respond",
        json={"session_id": session_id, "message": "All done"},
    )

    # Verify response
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "complete"
    assert "sections" in data
    assert "introduction" in data["sections"]


def test_respond_missing_fields(client):
    """Test error handling for missing required fields."""
    response = client.post(
        "/api/v1/interactive/respond",
        json={"session_id": "123"},  # Missing message
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "session_id and message" in data["error"]


def test_respond_invalid_session(client):
    """Test error handling for invalid session ID."""
    response = client.post(
        "/api/v1/interactive/respond",
        json={"session_id": "invalid-id", "message": "Hello"},
    )

    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert "Invalid or expired" in data["error"]


def test_get_session_status(client, mocker):
    """Test retrieving session status."""
    # Start session
    mock_agent_class = mocker.patch("backend.ai.routes.InteractiveAgent")
    mock_agent = mock_agent_class.return_value

    mock_agent.start_conversation.return_value = {
        "message": "Hello!",
        "conversation_id": 12345,
        "progress": {"percentage": 0},
        "next_steps": [],
    }

    mock_agent._calculate_progress.return_value = {
        "percentage": 40,
        "completed_sections": ["project_overview", "functional_requirements"],
        "missing_sections": ["non_functional_requirements"],
        "total_sections": 5,
    }

    start_response = client.post("/api/v1/interactive/start")
    session_id = start_response.get_json()["session_id"]

    # Get status
    response = client.get(f"/api/v1/interactive/status/{session_id}")

    # Verify response
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "progress" in data
    assert data["progress"]["percentage"] == 40


def test_get_session_status_invalid(client):
    """Test error handling for invalid session status request."""
    response = client.get("/api/v1/interactive/status/invalid-id")

    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
