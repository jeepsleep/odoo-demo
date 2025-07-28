from __future__ import annotations

from functools import lru_cache

import httpx
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ──────────────────────────────
    #  MCP server
    # ──────────────────────────────
    DEPLOYMENT_MODE: str = Field(
        default="local",
        description="Deployment mode ('local' or 'production')"
    )
    MCP_SERVER_PORT: int = Field(
        default=3000,
        description="Port used by the MCP gateway (only used in local mode)"
    )
    MCP_SERVER_HOST: str = Field(
        default="0.0.0.0",
        description="Host used by the MCP gateway (only used in local mode)"
    )
    MCP_PRODUCTION_URL: str = Field(
        default="https://gms-mcp.foundation.vision",
        description="Production URL for the MCP gateway"
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging verbosity (DEBUG, INFO, WARNING, ERROR)"
    )

    
    # ──────────────────────────────
    #  Odoo connection
    # ──────────────────────────────
    ODOO_URL: str = Field(
        default=None, description="Odoo base URL"
    )
    ODOO_DB: str = Field(
        default=None, description="Odoo database name"
    )
    ODOO_USER: str = Field(
        default=None, description="Odoo username"
    )
    ODOO_PASS: str = Field(
        default=None, description="Odoo password"
    )

    def get_odoo_params(self) -> tuple[str, str, str, str]:
        """Return Odoo connection parameters as a tuple."""
        return (self.ODOO_URL, self.ODOO_DB, self.ODOO_USER, self.ODOO_PASS)


    # ──────────────────────────────
    # pydantic-settings config
    # ──────────────────────────────
    model_config = SettingsConfigDict(
        # carga primero de variables de entorno, luego de .env
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("DEPLOYMENT_MODE")
    @classmethod
    def validate_deployment_mode(cls, v: str) -> str:
        """Validate deployment mode value."""
        if v not in ["local", "production"]:
            raise ValueError("Input should be 'local' or 'production'")
        return v

    def get_base_url(self) -> str:
        """Get the base URL based on deployment mode."""
        if self.DEPLOYMENT_MODE == "production":
            return self.MCP_PRODUCTION_URL
        return f"http://{self.MCP_SERVER_HOST}:{self.MCP_SERVER_PORT}"


@lru_cache(maxsize=1)
def get_settings() -> Settings:  # pragma: no cover
    # Al llamar, pydantic leerá ENV vars, luego .env, luego defaults
    return Settings()


def get_http_client() -> httpx.AsyncClient:  # pragma: no cover
    """Create and return a configured HTTPX AsyncClient instance."""
    return httpx.AsyncClient(
        base_url=get_settings().get_base_url(),
        timeout=30.0,
        follow_redirects=True,
        headers={"Content-Type": "application/json"},
    )
