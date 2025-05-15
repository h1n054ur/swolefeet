"""Tests for the SearchSession class."""

import pytest
from datetime import datetime
from app.core.search_session import SearchSession
from app.models.phone_number import PhoneNumber

@pytest.mark.core
class TestSearchSession:
    """Test suite for SearchSession."""
    
    def test_deduplication_limit(self):
        """Test that deduplication stops at 500 unique numbers."""
        session = SearchSession()
        
        # Create 600 unique numbers
        for i in range(600):
            number = PhoneNumber(
                number=f"+1555000{i:04d}",
                friendly_name=f"Test {i}",
                city="Test City",
                state="TS",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            )
            session.add_number(number)
        
        # Verify only 500 were kept
        assert len(session.get_numbers()) == 500
        
        # Verify they're the first 500
        numbers = session.get_numbers()
        for i in range(500):
            assert numbers[i].number == f"+1555000{i:04d}"
    
    def test_empty_batch_limit(self):
        """Test that session stops after 3 empty batches."""
        session = SearchSession()
        
        # Add some numbers
        for i in range(5):
            number = PhoneNumber(
                number=f"+1555000{i:04d}",
                friendly_name=f"Test {i}",
                city="Test City",
                state="TS",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            )
            session.add_number(number)
        
        # Add 3 empty batches
        session.add_batch([])
        assert not session.should_stop()
        
        session.add_batch([])
        assert not session.should_stop()
        
        session.add_batch([])
        assert session.should_stop()
    
    def test_duplicate_handling(self):
        """Test that duplicates are properly handled."""
        session = SearchSession()
        
        # Add same number twice
        number = PhoneNumber(
            number="+15550001234",
            friendly_name="Test",
            city="Test City",
            state="TS",
            country="US",
            capabilities={"voice": True, "sms": True},
            added_at=datetime.now()
        )
        
        session.add_number(number)
        session.add_number(number)
        
        assert len(session.get_numbers()) == 1
    
    def test_batch_progress(self):
        """Test that batch progress is correctly tracked."""
        session = SearchSession()
        
        # Add 3 batches of different sizes
        batch1 = [
            PhoneNumber(
                number=f"+1555000{i:04d}",
                friendly_name=f"Test {i}",
                city="Test City",
                state="TS",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            )
            for i in range(5)
        ]
        
        batch2 = [
            PhoneNumber(
                number=f"+1555001{i:04d}",
                friendly_name=f"Test {i}",
                city="Test City",
                state="TS",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            )
            for i in range(3)
        ]
        
        batch3 = [
            PhoneNumber(
                number=f"+1555002{i:04d}",
                friendly_name=f"Test {i}",
                city="Test City",
                state="TS",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            )
            for i in range(2)
        ]
        
        session.add_batch(batch1)
        assert session.total_batches == 1
        assert session.total_numbers == 5
        
        session.add_batch(batch2)
        assert session.total_batches == 2
        assert session.total_numbers == 8
        
        session.add_batch(batch3)
        assert session.total_batches == 3
        assert session.total_numbers == 10