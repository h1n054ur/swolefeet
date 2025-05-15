"""Tests for the NumberService."""

import pytest
from unittest.mock import MagicMock, call
from datetime import datetime
from app.services.number_service import NumberService
from app.models.phone_number import PhoneNumber
from app.models.search_criteria import SearchCriteria

@pytest.mark.services
class TestNumberService:
    """Test suite for NumberService."""
    
    @pytest.fixture
    def mock_progress_callback(self):
        """Create a mock progress callback."""
        return MagicMock()
    
    def test_search_available_numbers(self, mock_twilio_gateway, mock_progress_callback):
        """Test searching for available numbers."""
        # Setup
        service = NumberService()
        service.gateway = mock_twilio_gateway
        
        # Mock search results in batches
        batch1 = [
            MagicMock(
                phone_number="+15550001111",
                friendly_name="Test 1",
                locality="City1",
                region="ST",
                iso_country="US",
                capabilities={"voice": True, "sms": True}
            ),
            MagicMock(
                phone_number="+15550002222",
                friendly_name="Test 2",
                locality="City2",
                region="ST",
                iso_country="US",
                capabilities={"voice": True, "sms": True}
            )
        ]
        
        batch2 = [
            MagicMock(
                phone_number="+15550003333",
                friendly_name="Test 3",
                locality="City3",
                region="ST",
                iso_country="US",
                capabilities={"voice": True, "sms": True}
            )
        ]
        
        mock_twilio_gateway.search_available_numbers.side_effect = [batch1, batch2, []]
        
        # Execute search
        criteria = SearchCriteria(
            area_code="555",
            contains="11",
            state="ST",
            country="US"
        )
        
        results = service.search_available_numbers(
            criteria=criteria,
            progress_callback=mock_progress_callback
        )
        
        # Verify results
        assert len(results) == 3
        assert results[0].number == "+15550001111"
        assert results[1].number == "+15550002222"
        assert results[2].number == "+15550003333"
        
        # Verify progress callbacks
        assert mock_progress_callback.call_count == 3
        mock_progress_callback.assert_has_calls([
            call(2, 1),  # First batch: 2 numbers
            call(3, 2),  # Second batch: 1 number
            call(3, 3)   # Third batch: 0 numbers
        ])
    
    def test_purchase_numbers_partial_success(self, mock_twilio_gateway):
        """Test purchasing numbers with partial success."""
        # Setup
        service = NumberService()
        service.gateway = mock_twilio_gateway
        
        numbers_to_buy = [
            PhoneNumber(
                number="+15550001111",
                friendly_name="Test 1",
                city="City1",
                state="ST",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            ),
            PhoneNumber(
                number="+15550002222",
                friendly_name="Test 2",
                city="City2",
                state="ST",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            ),
            PhoneNumber(
                number="+15550003333",
                friendly_name="Test 3",
                city="City3",
                state="ST",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            )
        ]
        
        # Mock purchase responses
        def mock_purchase(number, *args, **kwargs):
            if number == "+15550002222":
                raise Exception("Purchase failed")
            return MagicMock(
                phone_number=number,
                friendly_name=f"Purchased {number}",
                status="active"
            )
        
        mock_twilio_gateway.purchase_number.side_effect = mock_purchase
        
        # Execute purchase
        success, failed = service.purchase_numbers(numbers_to_buy)
        
        # Verify results
        assert len(success) == 2
        assert len(failed) == 1
        
        assert success[0].number == "+15550001111"
        assert success[1].number == "+15550003333"
        assert failed[0].number == "+15550002222"
        
        # Verify purchase attempts
        assert mock_twilio_gateway.purchase_number.call_count == 3
    
    def test_search_with_empty_results(self, mock_twilio_gateway, mock_progress_callback):
        """Test search with no results."""
        # Setup
        service = NumberService()
        service.gateway = mock_twilio_gateway
        
        # Mock empty search results
        mock_twilio_gateway.search_available_numbers.return_value = []
        
        # Execute search
        criteria = SearchCriteria(
            area_code="999",  # Non-existent area code
            state="ZZ",
            country="US"
        )
        
        results = service.search_available_numbers(
            criteria=criteria,
            progress_callback=mock_progress_callback
        )
        
        # Verify results
        assert len(results) == 0
        
        # Verify progress callback
        mock_progress_callback.assert_called_once_with(0, 1)
    
    def test_search_with_error(self, mock_twilio_gateway):
        """Test search with error."""
        # Setup
        service = NumberService()
        service.gateway = mock_twilio_gateway
        
        # Mock search error
        mock_twilio_gateway.search_available_numbers.side_effect = Exception("Search failed")
        
        # Execute and verify
        criteria = SearchCriteria(
            area_code="555",
            state="ST",
            country="US"
        )
        
        with pytest.raises(Exception) as exc:
            service.search_available_numbers(criteria)
        
        assert "Search failed" in str(exc.value)
    
    def test_purchase_with_invalid_number(self, mock_twilio_gateway):
        """Test purchase with invalid number format."""
        # Setup
        service = NumberService()
        service.gateway = mock_twilio_gateway
        
        invalid_number = PhoneNumber(
            number="invalid",  # Invalid format
            friendly_name="Test",
            city="City",
            state="ST",
            country="US",
            capabilities={"voice": True, "sms": True},
            added_at=datetime.now()
        )
        
        # Execute purchase
        success, failed = service.purchase_numbers([invalid_number])
        
        # Verify results
        assert len(success) == 0
        assert len(failed) == 1
        assert failed[0].number == "invalid"
        
        # Verify no purchase attempt was made
        mock_twilio_gateway.purchase_number.assert_not_called()