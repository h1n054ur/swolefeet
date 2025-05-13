"""Test configuration and fixtures."""

import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_twilio_client():
    """Mock the Twilio client for all tests."""
    with patch('twilio.rest.Client') as mock:
        yield mock

@pytest.fixture(autouse=True)
def mock_console():
    """Mock the Rich console for all tests."""
    with patch('rich.console.Console') as mock:
        yield mock

@pytest.fixture(autouse=True)
def mock_clear_screen():
    """Mock screen clearing for all tests."""
    with patch('twilio_manager.shared.ui.styling.clear_screen') as mock:
        yield mock

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for all tests."""
    monkeypatch.setenv('TWILIO_ACCOUNT_SID', 'test_account_sid')
    monkeypatch.setenv('TWILIO_AUTH_TOKEN', 'test_auth_token')
    monkeypatch.setenv('TWILIO_PHONE_NUMBER', '+1234567890')