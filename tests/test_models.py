"""Tests for data models and validation."""

import pytest
from decimal import Decimal
from datetime import datetime
from app.models.data_models import (
    NumberType, NumberRecord, SearchSession,
    UsageStats, LogDirection, LogStatus, LogEntry
)
from app.models.validation import (
    is_valid_country, is_valid_region,
    is_valid_number_type, is_valid_area_code,
    is_valid_capability_set, is_valid_e164,
    normalize_number
)
from app.models.country_data import (
    get_area_codes, get_country_name,
    get_number_types, get_regions
)

def test_number_record():
    """Test NumberRecord validation."""
    # Valid record
    record = NumberRecord(
        number='+12125551234',
        city='New York',
        state='NY',
        type=NumberType.LOCAL,
        price=Decimal('1.15')
    )
    assert record.number == '+12125551234'
    assert record.type == NumberType.LOCAL
    
    # Invalid number format
    with pytest.raises(ValueError):
        NumberRecord(
            number='12125551234',  # Missing +
            type=NumberType.LOCAL,
            price=Decimal('1.15')
        )

def test_search_session():
    """Test SearchSession validation."""
    session = SearchSession(
        unique_count=10,
        empty_streaks=2,
        batches=5
    )
    assert session.unique_count == 10
    
    # Test negative values
    with pytest.raises(ValueError):
        SearchSession(unique_count=-1)

def test_usage_stats():
    """Test UsageStats validation."""
    stats = UsageStats(
        usage=100,
        cost=Decimal('115.00'),
        projection=Decimal('150.00')
    )
    assert stats.usage == 100
    assert stats.cost == Decimal('115.00')
    
    # Test negative values
    with pytest.raises(ValueError):
        UsageStats(
            usage=-1,
            cost=Decimal('115.00')
        )

def test_log_entry():
    """Test LogEntry validation."""
    entry = LogEntry(
        direction=LogDirection.INBOUND,
        status=LogStatus.SUCCESS,
        details='Test message'
    )
    assert isinstance(entry.timestamp, datetime)
    assert entry.direction == LogDirection.INBOUND
    assert entry.status == LogStatus.SUCCESS

def test_country_validation():
    """Test country code validation."""
    assert is_valid_country('US')
    assert is_valid_country('CA')
    assert not is_valid_country('XX')

def test_region_validation():
    """Test region validation."""
    assert is_valid_region('US', 'California')
    assert not is_valid_region('US', 'Invalid')
    assert not is_valid_region('XX', 'California')

def test_number_type_validation():
    """Test number type validation."""
    assert is_valid_number_type('US', 'local')
    assert is_valid_number_type('US', 'tollfree')
    assert not is_valid_number_type('US', 'invalid')

def test_area_code_validation():
    """Test area code validation."""
    assert is_valid_area_code('US', 212)  # NYC
    assert not is_valid_area_code('US', 999)

def test_capability_validation():
    """Test capability validation."""
    assert is_valid_capability_set({'voice', 'SMS'})
    assert not is_valid_capability_set({'invalid'})

def test_e164_validation():
    """Test E.164 number validation."""
    assert is_valid_e164('+12125551234')
    assert not is_valid_e164('12125551234')
    assert not is_valid_e164('+abc')

def test_number_normalization():
    """Test phone number normalization."""
    assert normalize_number('(212) 555-1234') == '+12125551234'
    assert normalize_number('+1-212-555-1234') == '+12125551234'
    
    with pytest.raises(ValueError):
        normalize_number('invalid')