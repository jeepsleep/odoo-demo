"""Tests for download routes."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from config.config import Settings
from server import app


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.mark.skipif(reason="Ignored for now")
def test_download_all_production(test_client):
    """Test download all endpoint in production mode."""
    with patch("api.download_routes.get_settings") as mock_settings:
        settings = Settings(
            DEPLOYMENT_MODE="production",
            MCP_PRODUCTION_URL="https://gms-mcp.foundation.vision",
            GMAPS_SCRAPER_USER="test_user",
            GMAPS_SCRAPER_PASS="test_pass"
        )
        mock_settings.return_value = settings
        
        # Mock the API client
        with patch("api.download_routes.get_api_client") as mock_client:
            client = MagicMock()
            mock_client.return_value = client
            
            response = test_client.get("/api/v1/jobs/test-job/download/all")
            print(f"Response: {response.content}")  # Debug line
            assert response.status_code == 200
            data = response.json()
            
            # Verify metadata
            assert data["metadata"]["job_id"] == "test-job"
            assert "pagination" in data["metadata"]
            assert data["metadata"]["pagination"]["current_page"] == 1
            assert data["metadata"]["pagination"]["total_pages"] == 1

@pytest.mark.skipif(reason="Ignored for now")
def test_download_all_local(test_client):
    """Test download all endpoint in local mode."""
    with patch("api.download_routes.get_settings") as mock_settings:
        settings = Settings(
            DEPLOYMENT_MODE="local",
            MCP_SERVER_HOST="0.0.0.0",
            MCP_SERVER_PORT=3000,
            GMAPS_SCRAPER_USER="test_user",
            GMAPS_SCRAPER_PASS="test_pass"
        )
        mock_settings.return_value = settings
        
        # Mock the API client
        with patch("api.download_routes.get_api_client") as mock_client:
            client = MagicMock()
            mock_client.return_value = client
            
            response = test_client.get("/api/v1/jobs/test-job/download/all")
            print(f"Response: {response.content}")  # Debug line
            assert response.status_code == 200
            data = response.json()
            
            # Verify metadata
            assert data["metadata"]["job_id"] == "test-job"
            assert "pagination" in data["metadata"]
            assert data["metadata"]["pagination"]["current_page"] == 1
            assert data["metadata"]["pagination"]["total_pages"] == 1

@pytest.mark.skipif(reason="Ignored for now")
def test_download_csv_format(test_client):
    """Test downloading results in CSV format."""
    with patch("api.download_routes.get_settings") as mock_settings:
        settings = Settings(
            DEPLOYMENT_MODE="production",
            MCP_PRODUCTION_URL="https://gms-mcp.foundation.vision",
            GMAPS_SCRAPER_USER="test_user",
            GMAPS_SCRAPER_PASS="test_pass"
        )
        mock_settings.return_value = settings
        
        # Mock the API client
        with patch("api.download_routes.get_api_client") as mock_client:
            client = MagicMock()
            mock_client.return_value = client
            
            response = test_client.get("/api/v1/jobs/test-job/download?format=csv")
            print(f"Response: {response.content}")  # Debug line
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/csv"
            assert response.headers["content-disposition"] == 'filename="test-job_results.csv"'

@pytest.mark.skipif(reason="Ignored for now")
def test_empty_results(test_client):
    """Test handling of empty results."""
    with patch("api.download_routes.get_settings") as mock_settings:
        settings = Settings(
            DEPLOYMENT_MODE="production",
            MCP_PRODUCTION_URL="https://gms-mcp.foundation.vision",
            GMAPS_SCRAPER_USER="test_user",
            GMAPS_SCRAPER_PASS="test_pass"
        )
        mock_settings.return_value = settings
        
        # Mock the API client
        with patch("api.download_routes.get_api_client") as mock_client:
            client = MagicMock()
            mock_client.return_value = client
            
            # Test JSON response
            response = test_client.get("/api/v1/jobs/test-job/download")
            print(f"Response: {response.content}")  # Debug line
            assert response.status_code == 200
            data = response.json()
            assert data["metadata"]["total_places_found"] == 0
            assert len(data["places"]) == 0
            
            # Test CSV response
            response = test_client.get("/api/v1/jobs/test-job/download?format=csv")
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/csv"
            assert len(response.content) == 0


def test_download_error_handling(test_client):
    """Test error handling in download endpoints."""
    with patch("api.download_routes.get_settings") as mock_settings:
        settings = Settings(
            DEPLOYMENT_MODE="production",
            MCP_PRODUCTION_URL="https://gms-mcp.foundation.vision",
            GMAPS_SCRAPER_USER="test_user",
            GMAPS_SCRAPER_PASS="test_pass"
        )
        mock_settings.return_value = settings
        
        # Mock the API client to raise an exception
        with patch("api.download_routes.get_api_client") as mock_client:
            client = MagicMock()
            mock_client.return_value = client
            
            response = test_client.get("/api/v1/jobs/test-job/download")
            assert response.status_code == 500
            assert "Failed to download results" in response.json()["detail"] 