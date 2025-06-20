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

def test_health_check_endpoint(client):
    """Test that health check endpoint returns correct response."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_metrics_endpoint(client):
    """Test that metrics endpoint returns Prometheus metrics."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.content_type == "text/plain; charset=utf-8"
    # Check if response contains expected metric names
    response_text = response.data.decode("utf-8")
    assert "srs_request_total" in response_text
    assert "srs_request_latency_seconds" in response_text
