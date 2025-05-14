"""Test suite for phone service."""

import pytest
from unittest.mock import Mock, patch
from twilio.base.exceptions import TwilioRestException
from twilio_manager.services.phone_service import PhoneService

# Mock data
MOCK_NUMBER = {
    "phone_number": "+1234567890",
    "friendly_name": "Test Number",
    "locality": "Test City",
    "region": "Test Region",
    "capabilities": {
        "voice": True,
        "sms": True,
        "mms": False
    },
    "monthly_rate": 1.15
}

@pytest.fixture
def phone_service():
    """Create a phone service instance with mocked client."""
    service = PhoneService()
    service.client = Mock()
    return service

def test_search_numbers(phone_service):
    """Test searching for available numbers."""
    # Mock API response
    mock_response = Mock()
    mock_response.json.return_value = {
        "available_phone_numbers": [MOCK_NUMBER]
    }
    mock_response.raise_for_status.return_value = None
    
    with patch('requests.get', return_value=mock_response):
        results = phone_service.search_numbers(
            country_code="US",
            number_type="local",
            capabilities=["VOICE", "SMS"]
        )
        
        assert len(results) == 1
        assert results[0]["phoneNumber"] == MOCK_NUMBER["phone_number"]
        assert results[0]["capabilities"]["voice"] == MOCK_NUMBER["capabilities"]["voice"]

def test_search_numbers_error(phone_service):
    """Test error handling in number search."""
    with patch('requests.get', side_effect=Exception("API Error")):
        results = phone_service.search_numbers(
            country_code="US",
            number_type="local",
            capabilities=["VOICE", "SMS"]
        )
        assert results == []

def test_purchase_number(phone_service):
    """Test purchasing a phone number."""
    # Mock successful purchase
    phone_service.client.incoming_phone_numbers.create.return_value = Mock(sid="test_sid")
    
    result = phone_service.purchase_number("+1234567890")
    assert result is True
    
    # Mock failed purchase
    phone_service.client.incoming_phone_numbers.create.side_effect = TwilioRestException(
        uri="test", msg="Purchase failed", code=400, status=400, method="POST"
    )
    
    result = phone_service.purchase_number("+1234567890")
    assert result is False

def test_configure_number(phone_service):
    """Test configuring a phone number."""
    # Mock number list
    mock_number = Mock(
        sid="test_sid",
        phone_number="+1234567890"
    )
    phone_service.client.incoming_phone_numbers.list.return_value = [mock_number]
    
    # Mock update
    mock_update = Mock(return_value=True)
    phone_service.client.incoming_phone_numbers.return_value.update = mock_update
    
    result = phone_service.configure_number(
        "+1234567890",
        friendly_name="Test Number",
        voice_url="http://test.com/voice",
        sms_url="http://test.com/sms"
    )
    assert result is True

def test_release_number(phone_service):
    """Test releasing a phone number."""
    # Mock number list
    mock_number = Mock(
        sid="test_sid",
        phone_number="+1234567890"
    )
    phone_service.client.incoming_phone_numbers.list.return_value = [mock_number]
    
    # Mock delete
    mock_delete = Mock(return_value=True)
    phone_service.client.incoming_phone_numbers.return_value.delete = mock_delete
    
    result = phone_service.release_number("+1234567890")
    assert result is True

def test_get_active_numbers(phone_service):
    """Test getting active phone numbers."""
    # Mock number list
    mock_number = Mock(
        sid="test_sid",
        phone_number="+1234567890",
        friendly_name="Test Number",
        capabilities={"voice": True, "sms": True, "mms": False},
        voice_url="http://test.com/voice",
        sms_url="http://test.com/sms"
    )
    phone_service.client.incoming_phone_numbers.list.return_value = [mock_number]
    
    results = phone_service.get_active_numbers()
    assert len(results) == 1
    assert results[0]["phoneNumber"] == "+1234567890"
    assert results[0]["capabilities"]["voice"] is True

def test_price_mapping(phone_service):
    """Test price mapping for different number types."""
    # Test US local number
    assert phone_service.PRICE_MAP[("US", "local")] == 1.15
    
    # Test UK toll-free number
    assert phone_service.PRICE_MAP[("GB", "tollfree")] == 2.15
    
    # Test AU mobile number
    assert phone_service.PRICE_MAP[("AU", "mobile")] == 6.50

def test_number_formatting(phone_service):
    """Test phone number formatting."""
    formatted = phone_service._format_phone_number_dict(
        MOCK_NUMBER,
        country="US",
        number_type="local"
    )
    
    assert formatted["phoneNumber"] == MOCK_NUMBER["phone_number"]
    assert formatted["friendlyName"] == MOCK_NUMBER["friendly_name"]
    assert formatted["region"] == MOCK_NUMBER["locality"]
    assert formatted["capabilities"]["voice"] is True
    assert formatted["monthlyPrice"] == 1.15

def test_error_handling(phone_service):
    """Test error handling in various scenarios."""
    # Test invalid number type
    results = phone_service.search_numbers(
        country_code="US",
        number_type="invalid",
        capabilities=[]
    )
    assert results == []
    
    # Test rate limiting
    with patch('requests.get') as mock_get:
        mock_get.side_effect = [
            Mock(status_code=429),  # Rate limit error
            Mock(  # Successful retry
                status_code=200,
                json=lambda: {"available_phone_numbers": [MOCK_NUMBER]}
            )
        ]
        
        results = phone_service.search_numbers(
            country_code="US",
            number_type="local",
            capabilities=[]
        )
        assert len(results) == 1