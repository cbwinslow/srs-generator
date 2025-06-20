import pytest
from backend.app import create_app
from backend.config import TestingConfig

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
    assert response.content_type == "text/plain"
    assert b"srs_request_total" in response.data
    assert b"srs_request_latency_seconds" in response.data
