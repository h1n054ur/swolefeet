"""Tests for the logging system."""

import os
import shutil
import logging
import pytest
from pathlib import Path
from twilio_manager.shared.utils.logger import get_logger

@pytest.fixture(autouse=True)
def cleanup_logs():
    """Clean up log files before and after each test."""
    log_dir = Path("logs").absolute()
    if log_dir.exists():
        shutil.rmtree(log_dir)
    log_dir.mkdir(parents=True)
    yield
    if log_dir.exists():
        shutil.rmtree(log_dir)

def test_logger_creation():
    """Test that the logger is created correctly."""
    logger = get_logger("test")
    assert logger.name == "twilio_manager.test"
    assert logger.level == logging.DEBUG
    
    # Check handlers
    assert len(logger.handlers) > 0
    has_file_handler = any(isinstance(h, logging.FileHandler) for h in logger.handlers)
    has_console_handler = any(isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler) for h in logger.handlers)
    assert has_file_handler, "File handler not found"
    assert has_console_handler, "Console handler not found"

def test_log_file_creation():
    """Test that log files are created in the correct location."""
    logger = get_logger("test_file")
    test_message = "Test log message"
    logger.info(test_message)
    
    # Check log file exists and contains message
    log_file = Path("logs/app.log").absolute()
    assert log_file.exists(), "Log file was not created"
    assert log_file.is_file(), "Log file path exists but is not a file"
    
    with open(log_file) as f:
        content = f.read()
        assert test_message in content, "Test message not found in log file"

def test_log_levels():
    """Test that different log levels work correctly."""
    logger = get_logger("test_levels")
    log_file = Path("logs/app.log").absolute()
    
    # Clear the log file
    with open(log_file, 'w') as f:
        f.write("")
    
    # Test messages
    debug_msg = "Debug test message"
    info_msg = "Info test message"
    warning_msg = "Warning test message"
    error_msg = "Error test message"
    
    # Log messages
    logger.debug(debug_msg)
    logger.info(info_msg)
    logger.warning(warning_msg)
    logger.error(error_msg)
    
    # Check log file content
    with open(log_file) as f:
        content = f.read()
        assert debug_msg in content, "Debug message not found"
        assert info_msg in content, "Info message not found"
        assert warning_msg in content, "Warning message not found"
        assert error_msg in content, "Error message not found"