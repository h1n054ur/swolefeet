"""Tests for VoiceService and MessagingService."""

import pytest
from unittest.mock import MagicMock
from app.services.voice_service import VoiceService
from app.services.messaging_service import MessagingService
from app.models.call import Call
from app.models.message import Message

@pytest.mark.services
class TestVoiceService:
    """Test suite for VoiceService."""
    
    def test_make_call(self, mock_twilio_gateway):
        """Test making a call."""
        # Setup
        service = VoiceService()
        service.gateway = mock_twilio_gateway
        
        # Mock call response
        mock_call = MagicMock(
            sid="CA123",
            from_="+15550001111",
            to="+15550002222",
            status="queued",
            direction="outbound-api"
        )
        mock_twilio_gateway.make_call.return_value = mock_call
        
        # Execute call
        call = service.make_call(
            from_number="+15550001111",
            to_number="+15550002222",
            url="http://example.com/twiml"
        )
        
        # Verify call
        assert isinstance(call, Call)
        assert call.sid == "CA123"
        assert call.from_number == "+15550001111"
        assert call.to_number == "+15550002222"
        assert call.status == "queued"
        
        # Verify gateway call
        mock_twilio_gateway.make_call.assert_called_once_with(
            from_number="+15550001111",
            to_number="+15550002222",
            url="http://example.com/twiml"
        )
    
    def test_get_call_status(self, mock_twilio_gateway):
        """Test getting call status."""
        # Setup
        service = VoiceService()
        service.gateway = mock_twilio_gateway
        
        # Mock status response
        mock_call = MagicMock(
            sid="CA123",
            from_="+15550001111",
            to="+15550002222",
            status="completed",
            direction="outbound-api",
            duration="60"
        )
        mock_twilio_gateway.get_call.return_value = mock_call
        
        # Execute status check
        status = service.get_call_status("CA123")
        
        # Verify status
        assert status == "completed"
        
        # Verify gateway call
        mock_twilio_gateway.get_call.assert_called_once_with("CA123")

@pytest.mark.services
class TestMessagingService:
    """Test suite for MessagingService."""
    
    def test_send_sms(self, mock_twilio_gateway):
        """Test sending an SMS."""
        # Setup
        service = MessagingService()
        service.gateway = mock_twilio_gateway
        
        # Mock message response
        mock_message = MagicMock(
            sid="SM123",
            from_="+15550001111",
            to="+15550002222",
            body="Test message",
            status="queued",
            direction="outbound-api"
        )
        mock_twilio_gateway.send_message.return_value = mock_message
        
        # Execute send
        message = service.send_sms(
            from_number="+15550001111",
            to_number="+15550002222",
            body="Test message"
        )
        
        # Verify message
        assert isinstance(message, Message)
        assert message.sid == "SM123"
        assert message.from_number == "+15550001111"
        assert message.to_number == "+15550002222"
        assert message.body == "Test message"
        assert message.status == "queued"
        
        # Verify gateway call
        mock_twilio_gateway.send_message.assert_called_once_with(
            from_number="+15550001111",
            to_number="+15550002222",
            body="Test message"
        )
    
    def test_get_message_status(self, mock_twilio_gateway):
        """Test getting message status."""
        # Setup
        service = MessagingService()
        service.gateway = mock_twilio_gateway
        
        # Mock status response
        mock_message = MagicMock(
            sid="SM123",
            from_="+15550001111",
            to="+15550002222",
            body="Test message",
            status="delivered",
            direction="outbound-api"
        )
        mock_twilio_gateway.get_message.return_value = mock_message
        
        # Execute status check
        status = service.get_message_status("SM123")
        
        # Verify status
        assert status == "delivered"
        
        # Verify gateway call
        mock_twilio_gateway.get_message.assert_called_once_with("SM123")
    
    def test_send_sms_with_media(self, mock_twilio_gateway):
        """Test sending an SMS with media."""
        # Setup
        service = MessagingService()
        service.gateway = mock_twilio_gateway
        
        # Mock message response
        mock_message = MagicMock(
            sid="SM123",
            from_="+15550001111",
            to="+15550002222",
            body="Test message",
            status="queued",
            direction="outbound-api",
            media_url="http://example.com/image.jpg"
        )
        mock_twilio_gateway.send_message.return_value = mock_message
        
        # Execute send
        message = service.send_sms(
            from_number="+15550001111",
            to_number="+15550002222",
            body="Test message",
            media_url="http://example.com/image.jpg"
        )
        
        # Verify message
        assert isinstance(message, Message)
        assert message.sid == "SM123"
        assert message.media_url == "http://example.com/image.jpg"
        
        # Verify gateway call
        mock_twilio_gateway.send_message.assert_called_once_with(
            from_number="+15550001111",
            to_number="+15550002222",
            body="Test message",
            media_url="http://example.com/image.jpg"
        )