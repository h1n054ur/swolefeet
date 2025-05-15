"""Data models for phone number records."""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class NumberRecord:
    """Record of a phone number with its details."""
    number: str  # E.164 format phone number
    country: str  # ISO country code
    type: str  # local/mobile/tollfree
    capabilities: List[str]  # List of capabilities (voice/sms/mms)
    price: Optional[float] = None  # Monthly price
    region: Optional[str] = None  # Region/state code
    locality: Optional[str] = None  # City/locality
    rate_center: Optional[str] = None  # Rate center
    latitude: Optional[float] = None  # Geographic latitude
    longitude: Optional[float] = None  # Geographic longitude

@dataclass
class SearchSession:
    """Session data for number search operations."""
    unique_count: int  # Count of unique numbers found
    empty_streaks: int  # Consecutive empty result batches
    batches: int  # Total search batches performed
    last_number: Optional[str] = None  # Last number found
    last_region: Optional[str] = None  # Last region searched

@dataclass
class LogEntry:
    """Log entry for number operations."""
    timestamp: str  # ISO format timestamp
    operation: str  # Operation type (purchase/release/etc)
    number: str  # Phone number involved
    status: str  # Operation status (success/failed)
    details: dict  # Additional operation details
