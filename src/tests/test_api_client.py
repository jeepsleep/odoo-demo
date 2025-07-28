# Tests de usuario únicamente

import pytest
from api.api_client import GMapsAPIClient


@pytest.fixture
def api_client():
    """Create a test API client."""
    return GMapsAPIClient("test_user", "test_pass")


# Eliminar todas las funciones relacionadas con create_job, delete_job, get_job y list_jobs
def test_placeholder():
    pass


def test_invalid_credentials():
    """Test client initialization with invalid credentials."""
    with pytest.raises(ValueError):
        GMapsAPIClient("", "password")
    
    with pytest.raises(ValueError):
        GMapsAPIClient("username", "") 