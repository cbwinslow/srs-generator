import pytest
from backend.app import create_app
from backend.config import TestingConfig

def test_create_app():
    """Test application factory."""
    assert create_app(TestingConfig) is not None

def test_config():
    """Test that config values are set correctly."""
    app = create_app(TestingConfig)
    assert app.config["TESTING"] is True
    assert app.config["DEBUG"] is True
