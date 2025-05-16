"""Tests for sorting utilities."""

import pytest
from datetime import datetime
from app.core.sorting import sort_numbers
from app.models.phone_number import PhoneNumber

@pytest.mark.core
class TestSorting:
    """Test suite for sorting utilities."""
    
    @pytest.fixture
    def sample_numbers(self):
        """Create a sample list of phone numbers."""
        return [
            PhoneNumber(
                number="+15550003333",
                friendly_name="Test 3",
                city="Chicago",
                state="IL",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            ),
            PhoneNumber(
                number="+15550001111",
                friendly_name="Test 1",
                city="Atlanta",
                state="GA",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            ),
            PhoneNumber(
                number="+15550002222",
                friendly_name="Test 2",
                city="Boston",
                state="MA",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            )
        ]
    
    def test_sort_by_number_ascending(self, sample_numbers):
        """Test sorting by number in ascending order."""
        sorted_numbers = sort_numbers(sample_numbers, "number", ascending=True)
        
        assert len(sorted_numbers) == 3
        assert sorted_numbers[0].number == "+15550001111"
        assert sorted_numbers[1].number == "+15550002222"
        assert sorted_numbers[2].number == "+15550003333"
    
    def test_sort_by_number_descending(self, sample_numbers):
        """Test sorting by number in descending order."""
        sorted_numbers = sort_numbers(sample_numbers, "number", ascending=False)
        
        assert len(sorted_numbers) == 3
        assert sorted_numbers[0].number == "+15550003333"
        assert sorted_numbers[1].number == "+15550002222"
        assert sorted_numbers[2].number == "+15550001111"
    
    def test_sort_by_city_ascending(self, sample_numbers):
        """Test sorting by city in ascending order."""
        sorted_numbers = sort_numbers(sample_numbers, "city", ascending=True)
        
        assert len(sorted_numbers) == 3
        assert sorted_numbers[0].city == "Atlanta"
        assert sorted_numbers[1].city == "Boston"
        assert sorted_numbers[2].city == "Chicago"
    
    def test_sort_by_city_descending(self, sample_numbers):
        """Test sorting by city in descending order."""
        sorted_numbers = sort_numbers(sample_numbers, "city", ascending=False)
        
        assert len(sorted_numbers) == 3
        assert sorted_numbers[0].city == "Chicago"
        assert sorted_numbers[1].city == "Boston"
        assert sorted_numbers[2].city == "Atlanta"
    
    def test_sort_with_empty_list(self):
        """Test sorting an empty list."""
        sorted_numbers = sort_numbers([], "number", ascending=True)
        assert sorted_numbers == []
    
    def test_sort_with_invalid_field(self, sample_numbers):
        """Test sorting with an invalid field."""
        with pytest.raises(ValueError):
            sort_numbers(sample_numbers, "invalid_field", ascending=True)
    
    def test_sort_with_none_values(self):
        """Test sorting with None values."""
        numbers = [
            PhoneNumber(
                number="+15550001111",
                friendly_name="Test 1",
                city=None,
                state="GA",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            ),
            PhoneNumber(
                number="+15550002222",
                friendly_name="Test 2",
                city="Boston",
                state="MA",
                country="US",
                capabilities={"voice": True, "sms": True},
                added_at=datetime.now()
            )
        ]
        
        sorted_numbers = sort_numbers(numbers, "city", ascending=True)
        assert len(sorted_numbers) == 2
        assert sorted_numbers[0].city is None
        assert sorted_numbers[1].city == "Boston"