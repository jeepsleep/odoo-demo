"""Common test fixtures for MCP tools."""

import pytest


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
def mock_api_client():
    """Create a mock API client."""
    return Mock(spec=GMapsAPIClient)


@pytest.fixture
def mcp():
    """Create a mock MCP instance."""
    return MockMCP() 