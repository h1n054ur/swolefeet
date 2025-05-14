"""Test suite for CLI menu system."""

import pytest
from unittest.mock import Mock, patch
from twilio_manager.shared.ui.registry import get_menu, menu_registry
from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.services.phone_service import PhoneService

# Mock data for testing
MOCK_PHONE_NUMBERS = [
    {
        "phoneNumber": "+1234567890",
        "friendlyName": "Test Number 1",
        "region": "US",
        "capabilities": {"voice": True, "sms": True, "mms": False},
        "monthlyPrice": 1.15
    },
    {
        "phoneNumber": "+0987654321",
        "friendlyName": "Test Number 2",
        "region": "UK",
        "capabilities": {"voice": True, "sms": True, "mms": True},
        "monthlyPrice": 2.15
    }
]

@pytest.fixture
def mock_phone_service():
    """Create a mock phone service."""
    with patch('twilio_manager.services.phone_service.PhoneService') as mock:
        service = Mock()
        service.search_numbers.return_value = MOCK_PHONE_NUMBERS
        service.purchase_number.return_value = True
        service.configure_number.return_value = True
        service.release_number.return_value = True
        service.get_active_numbers.return_value = MOCK_PHONE_NUMBERS
        mock.return_value = service
        yield service

@pytest.fixture
def mock_input():
    """Mock user input."""
    with patch('builtins.input') as mock:
        yield mock

@pytest.fixture
def mock_print():
    """Mock print function."""
    with patch('builtins.print') as mock:
        yield mock

def test_menu_registry():
    """Test that all required menus are in the registry."""
    required_menus = {
        "main", "phone", "messaging", "voice", "account", "advanced",
        "search", "search_parameters", "search_results", "purchase",
        "configure", "release", "send_message", "view_messages",
        "delete_message", "call", "call_confirm", "select_caller",
        "select_recipient", "select_voice_response", "conference",
        "recordings", "account_info", "api_keys", "sip_trunks",
        "subaccounts", "twiml_apps"
    }
    assert set(menu_registry.keys()) == required_menus

def test_menu_inheritance():
    """Test that all menus inherit from BaseMenu."""
    for menu_class in menu_registry.values():
        assert issubclass(menu_class, BaseMenu)

def test_menu_parent_child():
    """Test parent/child menu relationships."""
    parent = get_menu("main")
    child = get_menu("phone", parent=parent)
    assert child.parent == parent

def test_search_flow(mock_phone_service, mock_input):
    """Test the search menu flow."""
    # Mock user inputs for search parameters
    mock_input.side_effect = ["1", "1", "1", "1", ""]  # Country, Type, Capabilities, Pattern, Return
    
    # Start search flow
    menu = get_menu("search")
    menu.show()
    
    # Verify service calls
    mock_phone_service.search_numbers.assert_called_once()
    args = mock_phone_service.search_numbers.call_args[0]
    assert args[0] == "+1"  # Country code
    assert args[1] == "local"  # Number type
    assert set(args[2]) == {"VOICE", "SMS"}  # Capabilities

def test_purchase_flow(mock_phone_service, mock_input):
    """Test the purchase menu flow."""
    # Mock user inputs for purchase
    mock_input.side_effect = ["1", "y", ""]  # Select first number, Confirm, Return
    
    # Start purchase flow with pre-populated results
    menu = get_menu("purchase")
    menu.show()
    
    # Verify service calls
    mock_phone_service.purchase_number.assert_called_once_with(MOCK_PHONE_NUMBERS[0]["phoneNumber"])

def test_empty_results(mock_phone_service, mock_input, mock_print):
    """Test handling of empty search results."""
    # Mock empty results
    mock_phone_service.search_numbers.return_value = []
    
    # Mock user input
    mock_input.side_effect = ["1", "1", "1", "1", ""]  # Country, Type, Capabilities, Pattern, Return
    
    # Start search flow
    menu = get_menu("search")
    menu.show()
    
    # Verify empty results message
    mock_print.assert_any_call("No numbers found matching your criteria.")

def test_error_handling(mock_phone_service, mock_input, mock_print):
    """Test error handling in menus."""
    # Mock service error
    mock_phone_service.search_numbers.side_effect = Exception("API Error")
    
    # Mock user input
    mock_input.side_effect = ["1", "1", "1", "1", ""]  # Country, Type, Capabilities, Pattern, Return
    
    # Start search flow
    menu = get_menu("search")
    menu.show()
    
    # Verify error message
    mock_print.assert_any_call("Error searching for numbers: API Error")

def test_menu_navigation(mock_input):
    """Test menu navigation."""
    # Mock navigation through menus
    mock_input.side_effect = ["1", "0", "0"]  # Enter phone menu, Back to main, Exit
    
    # Start at main menu
    menu = get_menu("main")
    menu.show()
    
    # Verify input calls
    assert mock_input.call_count == 3

def test_invalid_input(mock_input, mock_print):
    """Test handling of invalid input."""
    # Mock invalid then valid input
    mock_input.side_effect = ["invalid", "1", "0"]
    
    # Start at main menu
    menu = get_menu("main")
    menu.show()
    
    # Verify error message
    mock_print.assert_any_call("Invalid choice. Please try again.")