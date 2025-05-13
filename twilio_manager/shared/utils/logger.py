"""
Centralized logging configuration for the Twilio Manager application.
Provides a consistent logging interface across all modules.
"""

import logging
import os
from pathlib import Path
from typing import Optional

# Constants
DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_CONSOLE_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class TwilioManagerLogger:
    _instance: Optional['TwilioManagerLogger'] = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        # Create base logger
        self.logger = logging.getLogger("twilio_manager")
        self.logger.setLevel(DEFAULT_LOG_LEVEL)
        
        # Ensure logs directory exists relative to the current working directory
        self.logs_dir = Path("logs").absolute()
        self.logs_dir.mkdir(exist_ok=True, parents=True)
        
        # Remove any existing handlers to avoid duplicates
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Set up handlers
        self._setup_handlers()
        
        # Prevent propagation to avoid duplicate logs
        self.logger.propagate = False
        
        self._initialized = True

    def _setup_handlers(self):
        """Set up file and console handlers with appropriate formatting."""
        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        
        # File handler - captures all logs
        file_handler = logging.FileHandler(self.logs_dir / "app.log", mode='a')
        file_handler.setLevel(DEFAULT_LOG_LEVEL)
        file_handler.setFormatter(formatter)
        
        # Console handler - shows INFO and above
        console_handler = logging.StreamHandler()
        console_handler.setLevel(DEFAULT_CONSOLE_LEVEL)
        console_handler.setFormatter(formatter)
        
        # Store handlers for reuse with child loggers
        self.file_handler = file_handler
        self.console_handler = console_handler
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self, name: str = None) -> logging.Logger:
        """
        Get a logger instance with the specified name.
        
        Args:
            name: Optional name to append to the base logger name
            
        Returns:
            logging.Logger: Configured logger instance
        """
        logger = self.logger
        if name:
            logger = self.logger.getChild(name)
            # Ensure child logger has the same handlers as parent
            if not logger.handlers:
                logger.addHandler(self.file_handler)
                logger.addHandler(self.console_handler)
        logger.setLevel(DEFAULT_LOG_LEVEL)  # Ensure child loggers inherit the correct level
        return logger

# Create the singleton instance
_logger_instance = TwilioManagerLogger()

# Convenience function to get a logger
def get_logger(name: str = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Optional name to append to the base logger name
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return _logger_instance.get_logger(name)

# Default logger instance for direct imports
logger = get_logger()