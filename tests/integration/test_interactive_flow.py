"""
Integration test for the interactive SRS generation flow.
This test validates the end-to-end interactive conversation flow.
"""
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


def test_complete_interactive_flow(client, mocker):
    """Test a complete interactive SRS generation flow from start to finish."""

    # Mock the InteractiveAgent class
    mock_agent_class = mocker.patch("backend.ai.routes.InteractiveAgent")
    mock_agent = mock_agent_class.return_value

    # Step 1: Start session
    mock_agent.start_conversation.return_value = {
        "message": "Hello! What is your project about?",
        "conversation_id": 99999,
        "progress": {
            "percentage": 0,
            "completed_sections": [],
            "missing_sections": [
                "project_overview",
                "functional_requirements",
                "non_functional_requirements",
                "user_interface",
                "technical_constraints",
            ],
            "total_sections": 5,
        },
        "next_steps": ["project_overview"],
    }

    response = client.post("/api/v1/interactive/start")
    assert response.status_code == 200
    data = response.get_json()
    session_id = data["session_id"]
    assert data["progress"]["percentage"] == 0

    # Step 2: First user response (project overview)
    mock_agent.process_user_input.return_value = {
        "message": "Great! What are the main features?",
        "collected_data": {"raw_notes": ["Mobile fitness tracking app"]},
        "progress": {"percentage": 20, "completed_sections": ["project_overview"]},
        "complete": False,
    }

    response = client.post(
        "/api/v1/interactive/respond",
        json={
            "session_id": session_id,
            "message": "I'm building a mobile fitness tracking app for health enthusiasts",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "in_progress"
    assert data["progress"]["percentage"] == 20

    # Step 3: Second response (functional requirements)
    mock_agent.process_user_input.return_value = {
        "message": "What are the performance requirements?",
        "collected_data": {
            "raw_notes": [
                "Mobile fitness tracking app",
                "Track workouts, calories, and progress",
            ]
        },
        "progress": {
            "percentage": 40,
            "completed_sections": ["project_overview", "functional_requirements"],
        },
        "complete": False,
    }

    response = client.post(
        "/api/v1/interactive/respond",
        json={
            "session_id": session_id,
            "message": "Users can track workouts, log calories, and view progress charts",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["progress"]["percentage"] == 40

    # Step 4: Third response (non-functional requirements)
    mock_agent.process_user_input.return_value = {
        "message": "What platforms will this run on?",
        "collected_data": {
            "raw_notes": [
                "Mobile fitness tracking app",
                "Track workouts, calories, and progress",
                "Fast loading, secure data, 99.9% uptime",
            ]
        },
        "progress": {"percentage": 60},
        "complete": False,
    }

    response = client.post(
        "/api/v1/interactive/respond",
        json={
            "session_id": session_id,
            "message": "Must be fast, secure user data, and have 99.9% uptime",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["progress"]["percentage"] == 60

    # Step 5: Fourth response (UI requirements)
    mock_agent.process_user_input.return_value = {
        "message": "Any technical constraints?",
        "collected_data": {
            "raw_notes": [
                "Mobile fitness tracking app",
                "Track workouts, calories, and progress",
                "Fast loading, secure data, 99.9% uptime",
                "iOS and Android with clean UI",
            ]
        },
        "progress": {"percentage": 80},
        "complete": False,
    }

    response = client.post(
        "/api/v1/interactive/respond",
        json={
            "session_id": session_id,
            "message": "iOS and Android with a clean, minimal UI",
        },
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["progress"]["percentage"] == 80

    # Step 6: Final response - triggers completion
    mock_agent.process_user_input.return_value = {
        "message": "Great! Generating your SRS document...",
        "collected_data": {
            "raw_notes": [
                "Mobile fitness tracking app",
                "Track workouts, calories, and progress",
                "Fast loading, secure data, 99.9% uptime",
                "iOS and Android with clean UI",
                "React Native, Firebase, AWS deployment",
            ]
        },
        "progress": {"percentage": 100},
        "complete": True,
    }

    # Mock the SRS generation
    mock_sections = {
        "introduction": "## Introduction\n\nThis is a fitness tracking mobile application...",
        "system_description": "## System Description\n\nThe system provides workout tracking...",
        "functional_requirements": (
            "## Functional Requirements\n\nFR1: Users shall be able to log workouts..."
        ),
        "non_functional_requirements": (
            "## Non-Functional Requirements\n\nNFR1: System shall load in under 2 seconds..."
        ),
        "user_interface": (
            "## User Interface\n\nThe app will have a clean, minimal iOS and Android interface..."
        ),
        "constraints": "## Constraints\n\nTechnical: React Native, Firebase backend...",
    }
    mock_agent.generate_complete_srs.return_value = mock_sections

    response = client.post(
        "/api/v1/interactive/respond",
        json={
            "session_id": session_id,
            "message": "React Native, Firebase backend, deploy on AWS",
        },
    )

    # Verify completion
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "complete"
    assert "sections" in data
    assert len(data["sections"]) == 6
    assert "introduction" in data["sections"]
    assert "functional_requirements" in data["sections"]

    # Verify the generate_complete_srs was called
    mock_agent.generate_complete_srs.assert_called_once()

    # Step 7: Check session status
    mock_agent._calculate_progress.return_value = {"percentage": 100}

    response = client.get(f"/api/v1/interactive/status/{session_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["progress"]["percentage"] == 100
