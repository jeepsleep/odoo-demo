"""Tests for server initialization and configuration."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from config.config import Settings
from server import app, create_app


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_create_app_production():
    """Test app creation in production mode."""
    with patch("server.get_settings") as mock_settings:
        settings = Settings(
            DEPLOYMENT_MODE="production",
            MCP_PRODUCTION_URL="https://gms-mcp.foundation.vision",
        )
        mock_settings.return_value = settings
        app = create_app()
        assert app is not None


def test_create_app_local():
    """Test app creation in local mode."""
    with patch("server.get_settings") as mock_settings:
        settings = Settings(
            DEPLOYMENT_MODE="local",
            MCP_SERVER_HOST="0.0.0.0",
            MCP_SERVER_PORT=3000,
        )
        mock_settings.return_value = settings
        app = create_app()
        assert app is not None

@pytest.mark.skipif(reason="Skip si se cumple la condición")
def test_download_url_production(test_client):
    """Test download URL generation in production mode."""
    with patch("api.download_routes.get_settings") as mock_settings:
        settings = Settings(
            DEPLOYMENT_MODE="production",
            MCP_PRODUCTION_URL="https://gms-mcp.foundation.vision",
        )
        mock_settings.return_value = settings
        
        # Mock the API client to avoid actual API calls
        with patch("api.download_routes.get_api_client") as mock_client:
            client = MagicMock()
            mock_client.return_value = client
            
            response = test_client.get("/api/v1/jobs/test-job/download")
            assert response.status_code == 200
            data = response.json()
            
            # Check that URLs use production domain
            if "pagination" in data["metadata"]:
                next_url = data["metadata"]["pagination"].get("next_page_url")
                if next_url:
                    assert "https://gms-mcp.foundation.vision" in next_url


@pytest.mark.skipif(reason="Skip si se cumple la condición")
def test_download_url_local(test_client):
    """Test download URL generation in local mode."""
    with patch("api.download_routes.get_settings") as mock_settings:
        settings = Settings(
            DEPLOYMENT_MODE="local",
            MCP_SERVER_HOST="0.0.0.0",
            MCP_SERVER_PORT=3000,
        )
        mock_settings.return_value = settings
        
        # Mock the API client to avoid actual API calls
        with patch("api.download_routes.get_api_client") as mock_client:
            client = MagicMock()
            mock_client.return_value = client
            
            response = test_client.get("/api/v1/jobs/test-job/download")
            assert response.status_code == 200
            data = response.json()
            
            # Check that URLs use local domain
            if "pagination" in data["metadata"]:
                next_url = data["metadata"]["pagination"].get("next_page_url")
                if next_url:
                    assert "http://0.0.0.0:3000" in next_url


def test_missing_credentials():
    """Test app creation fails with missing credentials."""
    with patch("server.get_settings") as mock_settings:
        settings = Settings(
            DEPLOYMENT_MODE="production",
        )
        mock_settings.return_value = settings
        with pytest.raises(Exception, match="Missing API credentials"):
            create_app() 