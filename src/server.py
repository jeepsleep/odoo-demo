"""FastMCP gateway for the Google Maps Scraper REST API.

This module serves as the main entry point for the MCP (Mission Control Protocol) gateway
that interfaces with the Google Maps Scraper REST API. It handles:

1. Server configuration and initialization
2. API client setup and validation
3. Tool and resource registration
4. ASGI application setup for HTTP and SSE (Server-Sent Events)

The server can be run directly with Uvicorn or imported as an ASGI application.
"""

import logging
import sys
from typing import NoReturn

import uvicorn
from fastapi import HTTPException
from mcp.server.fastmcp import FastMCP

from config.config import get_settings
from tools import register_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app() -> FastMCP:
    """
    Create and configure the FastMCP application.

    Returns:
        FastMCP: The configured FastMCP application instance
    """
    # Initialize settings
    settings = get_settings()
    
    # Initialize FastMCP
    mcp = FastMCP(
        title="Odoo MCP",
        description="A MCP for Odoo",
        version="1.0.0"
    )
    
    # Register MCP tools
    try:
        register_tools(mcp)
        logger.info("Successfully registered MCP tools")
    except Exception as e:
        logger.error(f"Failed to register MCP components: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to initialize MCP components"
        ) from e
    
    return mcp
def run_server() -> NoReturn:
    """
    Run the server with Uvicorn.
    """
    settings = get_settings()
    
    if settings.DEPLOYMENT_MODE == "production":
        logger.info("Starting server in production mode")
        # In production, we assume the server is behind a reverse proxy
        # that handles the host/port configuration
        uvicorn.run(
            app,
            host="0.0.0.0",  # Listen on all interfaces
            port=3000,  # Use standard port, will be mapped by reverse proxy
            log_level=settings.LOG_LEVEL.lower()
        )
    else:
        # Local development mode
        logger.info(f"Starting server in local mode on {settings.MCP_SERVER_HOST}:{settings.MCP_SERVER_PORT}")
        uvicorn.run(
            app,
            host=settings.MCP_SERVER_HOST,
            port=settings.MCP_SERVER_PORT,
            log_level=settings.LOG_LEVEL.lower()
        )
    sys.exit(0)  # Ensure NoReturn type is satisfied

# Create ASGI application
try:
    mcp = create_app()
    # Mount FastAPI app under the MCP app
    app = mcp.streamable_http_app()

    logger.info("Successfully created ASGI application with API routes")
except Exception as e:
    logger.critical(f"Failed to create ASGI application: {str(e)}")
    raise

if __name__ == "__main__":  # pragma: no cover
    run_server()
