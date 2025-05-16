"""Configuration gateway for loading environment variables."""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from ..shared.settings import Settings

logger = logging.getLogger(__name__)

def load_settings() -> Settings:
    """Load application settings from environment variables.
    
    Returns:
        Settings object populated with values from environment.
    
    Raises:
        ValueError: If required environment variables are missing.
    """
    # Load .env file if it exists
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    
    # Required variables
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError as e:
        raise ValueError(f"Missing required environment variable: {e}")
    
    # Optional variables
    subaccount_sid = os.environ.get("TWILIO_SUBACCOUNT_SID")
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    
    settings = Settings(
        account_sid=account_sid,
        auth_token=auth_token,
        subaccount_sid=subaccount_sid,
        log_level=log_level
    )
    
    logger.debug("Settings loaded successfully")
    return settings
