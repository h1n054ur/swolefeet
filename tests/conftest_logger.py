"""Test configuration for logger tests."""

import pytest
import shutil
from pathlib import Path

@pytest.fixture(autouse=True)
def cleanup_logs():
    """Clean up log files before and after each test."""
    log_dir = Path("logs")
    if log_dir.exists():
        shutil.rmtree(log_dir)
    log_dir.mkdir()
    yield
    if log_dir.exists():
        shutil.rmtree(log_dir)