"""Logging configuration for the Twilio Manager CLI."""

import logging
import logging.handlers
from pathlib import Path
from pythonjsonlogger import jsonlogger
from .settings import Settings


def configure_logging(settings: Settings) -> None:
    """Configure application-wide logging.
    
    Args:
        settings: Application settings containing logging configuration.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)
    
    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler with standard formatting
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(settings.log_format))
    root_logger.addHandler(console_handler)
    
    # File handler with JSON formatting if log file is specified
    if settings.log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            settings.log_file,
            maxBytes=settings.log_max_bytes,
            backupCount=settings.log_backup_count
        )
        json_formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        file_handler.setFormatter(json_formatter)
        root_logger.addHandler(file_handler)
    
    # Suppress some chatty loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("twilio").setLevel(logging.INFO)