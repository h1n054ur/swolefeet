"""Tests for the Twilio gateway."""

import pytest
from unittest.mock import MagicMock
from twilio.base.exceptions import TwilioRestException
from app.gateways.twilio_gateway import TwilioGateway

@pytest.mark.services
class TestTwilioGateway:
    """Test suite for TwilioGateway."""
    
    def test_successful_api_call(self, mock_twilio_client):
        """Test successful API call."""
        # Setup
        gateway = TwilioGateway()
        gateway.client = mock_twilio_client
        
        # Mock successful response
        mock_twilio_client.incoming_phone_numbers.list.return_value = [
            MagicMock(phone_number="+15550001111"),
            MagicMock(phone_number="+15550002222")
        ]
        
        # Execute and verify
        numbers = gateway.list_numbers()
        assert len(numbers) == 2
        assert numbers[0].phone_number == "+15550001111"
        assert numbers[1].phone_number == "+15550002222"
    
    def test_failed_api_call(self, mock_twilio_client):
        """Test failed API call."""
        # Setup
        gateway = TwilioGateway()
        gateway.client = mock_twilio_client
        
        # Mock error response
        mock_twilio_client.incoming_phone_numbers.list.side_effect = TwilioRestException(
            uri="test",
            msg="Test error",
            code=400,
            status=400,
            method="GET"
        )
        
        # Execute and verify
        with pytest.raises(TwilioRestException) as exc:
            gateway.list_numbers()
        
        assert exc.value.status == 400
        assert "Test error" in str(exc.value)
    
    def test_rate_limit_handling(self, mock_twilio_client):
        """Test rate limit handling."""
        # Setup
        gateway = TwilioGateway()
        gateway.client = mock_twilio_client
        
        # Mock rate limit response
        mock_twilio_client.incoming_phone_numbers.list.side_effect = TwilioRestException(
            uri="test",
            msg="Too many requests",
            code=429,
            status=429,
            method="GET"
        )
        
        # Execute and verify
        with pytest.raises(TwilioRestException) as exc:
            gateway.list_numbers()
        
        assert exc.value.status == 429
        assert "Too many requests" in str(exc.value)
    
    def test_authentication_error(self, mock_twilio_client):
        """Test authentication error handling."""
        # Setup
        gateway = TwilioGateway()
        gateway.client = mock_twilio_client
        
        # Mock auth error response
        mock_twilio_client.incoming_phone_numbers.list.side_effect = TwilioRestException(
            uri="test",
            msg="Authentication failed",
            code=401,
            status=401,
            method="GET"
        )
        
        # Execute and verify
        with pytest.raises(TwilioRestException) as exc:
            gateway.list_numbers()
        
        assert exc.value.status == 401
        assert "Authentication failed" in str(exc.value)
    
    def test_network_error(self, mock_twilio_client):
        """Test network error handling."""
        # Setup
        gateway = TwilioGateway()
        gateway.client = mock_twilio_client
        
        # Mock network error
        mock_twilio_client.incoming_phone_numbers.list.side_effect = ConnectionError("Network error")
        
        # Execute and verify
        with pytest.raises(ConnectionError) as exc:
            gateway.list_numbers()
        
        assert "Network error" in str(exc.value)