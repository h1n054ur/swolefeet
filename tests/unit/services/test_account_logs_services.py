"""Tests for AccountService and LogsService."""

import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from app.services.account_service import AccountService
from app.services.log_service import LogService
from app.models.usage import Usage, UsageCategory
from app.models.billing import BillingInfo, Address
from app.models.log_entry import LogEntry

@pytest.mark.services
class TestAccountService:
    """Test suite for AccountService."""
    
    def test_get_usage(self, mock_twilio_gateway):
        """Test getting usage information."""
        # Setup
        service = AccountService()
        service.gateway = mock_twilio_gateway
        
        # Mock usage response
        mock_usage = {
            'voice': {
                'usage': 100,
                'cost': 10.50
            },
            'messaging': {
                'usage': 500,
                'cost': 25.00
            }
        }
        mock_twilio_gateway.get_usage.return_value = mock_usage
        
        # Execute
        usage = service.get_usage()
        
        # Verify
        assert isinstance(usage, Usage)
        assert len(usage.categories) == 2
        
        voice = next(c for c in usage.categories if c.name == 'voice')
        assert voice.usage == 100
        assert voice.cost == 10.50
        
        messaging = next(c for c in usage.categories if c.name == 'messaging')
        assert messaging.usage == 500
        assert messaging.cost == 25.00
        
        assert usage.total_cost == 35.50
    
    def test_get_billing(self, mock_twilio_gateway):
        """Test getting billing information."""
        # Setup
        service = AccountService()
        service.gateway = mock_twilio_gateway
        
        # Mock billing response
        mock_billing = {
            'type': 'credit_card',
            'payment_method': 'Visa ending in 1234',
            'email': 'test@example.com',
            'tax_id': 'TAX123',
            'address': {
                'street': '123 Main St',
                'city': 'Anytown',
                'state': 'ST',
                'country': 'US',
                'postal_code': '12345'
            }
        }
        mock_twilio_gateway.get_billing.return_value = mock_billing
        
        # Execute
        billing = service.get_billing()
        
        # Verify
        assert isinstance(billing, BillingInfo)
        assert billing.type == 'credit_card'
        assert billing.payment_method == 'Visa ending in 1234'
        assert billing.email == 'test@example.com'
        assert billing.tax_id == 'TAX123'
        
        assert isinstance(billing.address, Address)
        assert billing.address.street == '123 Main St'
        assert billing.address.city == 'Anytown'
        assert billing.address.state == 'ST'
        assert billing.address.country == 'US'
        assert billing.address.postal_code == '12345'
    
    def test_get_usage_history(self, mock_twilio_gateway):
        """Test getting usage history."""
        # Setup
        service = AccountService()
        service.gateway = mock_twilio_gateway
        
        # Mock history response
        mock_history = [
            {
                'date': '2023-01-01',
                'voice_minutes': 100,
                'sms_count': 500,
                'total_cost': 25.00
            },
            {
                'date': '2023-01-02',
                'voice_minutes': 150,
                'sms_count': 750,
                'total_cost': 37.50
            }
        ]
        mock_twilio_gateway.get_usage_history.return_value = mock_history
        
        # Execute
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 2)
        history = service.get_usage_history(start_date, end_date)
        
        # Verify
        assert len(history) == 2
        
        assert history[0].date == datetime(2023, 1, 1)
        assert history[0].voice_minutes == 100
        assert history[0].sms_count == 500
        assert history[0].total_cost == 25.00
        
        assert history[1].date == datetime(2023, 1, 2)
        assert history[1].voice_minutes == 150
        assert history[1].sms_count == 750
        assert history[1].total_cost == 37.50

@pytest.mark.services
class TestLogService:
    """Test suite for LogService."""
    
    def test_get_account_logs(self, mock_twilio_gateway):
        """Test getting account logs."""
        # Setup
        service = LogService()
        service.gateway = mock_twilio_gateway
        
        # Mock logs response
        mock_logs = [
            {
                'timestamp': '2023-01-01T12:00:00Z',
                'level': 'error',
                'service': 'voice',
                'message': 'Call failed',
                'resource_sid': 'CA123'
            },
            {
                'timestamp': '2023-01-01T12:01:00Z',
                'level': 'info',
                'service': 'messaging',
                'message': 'Message sent',
                'resource_sid': 'SM456'
            }
        ]
        mock_twilio_gateway.get_logs.return_value = mock_logs
        
        # Execute
        logs = service.get_account_logs(
            log_type='all',
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 1, 2)
        )
        
        # Verify
        assert len(logs) == 2
        
        assert isinstance(logs[0], LogEntry)
        assert logs[0].timestamp == datetime(2023, 1, 1, 12, 0)
        assert logs[0].level == 'error'
        assert logs[0].service == 'voice'
        assert logs[0].message == 'Call failed'
        assert logs[0].resource_sid == 'CA123'
        
        assert isinstance(logs[1], LogEntry)
        assert logs[1].timestamp == datetime(2023, 1, 1, 12, 1)
        assert logs[1].level == 'info'
        assert logs[1].service == 'messaging'
        assert logs[1].message == 'Message sent'
        assert logs[1].resource_sid == 'SM456'
    
    def test_get_logs_with_filtering(self, mock_twilio_gateway):
        """Test getting logs with type filtering."""
        # Setup
        service = LogService()
        service.gateway = mock_twilio_gateway
        
        # Mock logs response
        mock_logs = [
            {
                'timestamp': '2023-01-01T12:00:00Z',
                'level': 'error',
                'service': 'voice',
                'message': 'Call failed',
                'resource_sid': 'CA123'
            }
        ]
        mock_twilio_gateway.get_logs.return_value = mock_logs
        
        # Execute
        logs = service.get_account_logs(
            log_type='error',
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 1, 2)
        )
        
        # Verify
        assert len(logs) == 1
        assert logs[0].level == 'error'
        
        # Verify gateway call
        mock_twilio_gateway.get_logs.assert_called_once_with(
            log_type='error',
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 1, 2),
            page=1,
            page_size=50
        )
    
    def test_export_logs(self, mock_twilio_gateway):
        """Test exporting logs."""
        # Setup
        service = LogService()
        service.gateway = mock_twilio_gateway
        
        # Mock logs response
        mock_logs = [
            {
                'timestamp': '2023-01-01T12:00:00Z',
                'level': 'error',
                'service': 'voice',
                'message': 'Call failed',
                'resource_sid': 'CA123'
            },
            {
                'timestamp': '2023-01-01T12:01:00Z',
                'level': 'info',
                'service': 'messaging',
                'message': 'Message sent',
                'resource_sid': 'SM456'
            }
        ]
        mock_twilio_gateway.get_logs.return_value = mock_logs
        
        # Execute
        service.export_logs(
            filename='test_logs.csv',
            log_type='all',
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 1, 2)
        )
        
        # Verify gateway calls
        mock_twilio_gateway.get_logs.assert_called_once()
        # Note: We would also verify the file contents here in a real test