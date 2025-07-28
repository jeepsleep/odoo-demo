"""Tests for configuration settings."""

import pytest

from config.config import Settings


def test_default_settings():
    """Test default configuration settings."""
    settings = Settings()
    assert settings.DEPLOYMENT_MODE == "production"
    assert settings.MCP_SERVER_HOST == "0.0.0.0"
    assert settings.MCP_SERVER_PORT == 3000
    assert settings.MCP_PRODUCTION_URL == "https://gms-mcp.foundation.vision"


def test_get_base_url_production():
    """Test base URL generation in production mode."""
    settings = Settings(DEPLOYMENT_MODE="production")
    assert settings.get_base_url() == "https://gms-mcp.foundation.vision"


def test_get_base_url_local():
    """Test base URL generation in local mode."""
    settings = Settings(
        DEPLOYMENT_MODE="local",
        MCP_SERVER_HOST="127.0.0.1",
        MCP_SERVER_PORT=5000
    )
    assert settings.get_base_url() == "http://127.0.0.1:5000"


def test_invalid_deployment_mode():
    """Test that invalid deployment mode raises ValueError."""
    with pytest.raises(ValueError, match="Input should be 'local' or 'production'"):
        Settings(DEPLOYMENT_MODE="invalid") 