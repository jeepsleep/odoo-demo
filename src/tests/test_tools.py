"""Integration tests for MCP tools."""

from unittest.mock import MagicMock

import pytest

from config.config import Settings


class MockMCP:
    """Mock MCP class for testing."""
    
    def __init__(self):
        self.tools = {}
    
    def tool(self, name, description):
        """Mock tool decorator."""
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator


@pytest.fixture
def mcp():
    """Create a mock MCP instance."""
    return MockMCP()


@pytest.fixture
def mock_api_client():
    """Create a mock API client with settings."""
    client = MagicMock(spec=GMapsAPIClient)
    client.settings = Settings(
        DEPLOYMENT_MODE="production",
        MCP_PRODUCTION_URL="https://gms-mcp.foundation.vision",
        GMAPS_SCRAPER_USER="test_user",
        GMAPS_SCRAPER_PASS="test_pass"
    )
    return client


@pytest.fixture
def tools(mcp, mock_api_client):
    """Register and return all tools."""
    register_tools(mcp, mock_api_client)
    return mcp.tools


# Eliminar todos los bloques relacionados con create_job, delete_job, get_job y list_jobs
def test_placeholder():
    pass 