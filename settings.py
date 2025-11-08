"""This module defines a `Settings` class for managing configuration related to Keycloak authentication.

It uses Pydantic for settings management and validation, and `pydantic_settings` for handling environment variables.
"""

import os

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """The `Settings` class contains the following configuration fields.

    - `keycloak_token_url`: URL for obtaining the Keycloak access token.
    - `keycloak_userinfo_url`: URL for retrieving authenticated user information from Keycloak.
    - `keycloak_client_id`: The client ID for your identity provider.
    - `keycloak_client_secret`: The client secret for your identity provider.
    - `keycloak_grant_type`: The grant type used in the authentication flow.
    """

    # NOTE: Change localhost to keycloak if your streamlit app runs in a container
    keycloak_token_url: str = Field(
        default="http://localhost:8080/realms/minimal/protocol/openid-connect/token",
        description="Keycloak endpoint to obtain an access token (access_token).",
    )

    keycloak_userinfo_url: str = Field(
        default="http://localhost:8080/realms/minimal/protocol/openid-connect/userinfo",
        description="Keycloak endpoint to retrieve authenticated user information.",
    )

    keycloak_client_id: str = Field(
        default="minimal-client",
        description="client_id from your identity provider. Clients -> Credentials tab.",
    )

    keycloak_client_secret: str = Field(
        default="UYNCLIHdNXQS89BSsKmX7QxsGeIQyMrV",
        description="client secret from your identity provider. Clients -> Credentials tab",
    )

    keycloak_grant_type: str = Field(
        default="password",
        description="Grant type from your identity provider. Clients -> Credentials tab",
    )

    class Config:
        """Config class definition."""

        env_nested_delimiter = "__"
        env_file = ".env"

    @model_validator(mode="before")
    def declare_env_var(cls, values: dict):
        """Declare environment variable from class attributes if does not exist.

        Args:
            values (dict): settings values.

        Returns:
            values: settings values.
        """
        for k, v in values.items():
            if k.upper() not in os.environ:
                os.environ[k.upper()] = str(v)
        return values


settings = Settings()
