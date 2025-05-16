"""Configuration settings for the Twilio Manager CLI."""

from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class Settings:
    """Application settings and configuration."""
    
    # Twilio credentials
    account_sid: str
    auth_token: str
    
    # Optional subaccount SID if using one
    subaccount_sid: Optional[str] = None
    
    # Application paths
    app_dir: Path = Path(__file__).parent.parent
    log_dir: Path = app_dir.parent / "logs"
    
    # Logging configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[Path] = log_dir / "twilio_manager.log"
    log_max_bytes: int = 10 * 1024 * 1024  # 10MB
    log_backup_count: int = 5
    
    # Search configuration
    search_batch_size: int = 50
    search_max_numbers: int = 500
    search_rate_limit: float = 1.0  # seconds between requests
    search_empty_limit: int = 3  # stop after N empty results
    
    def __post_init__(self):
        """Ensure log directory exists."""
        self.log_dir.mkdir(parents=True, exist_ok=True)