"""Data models for Twilio Manager CLI."""

from datetime import datetime, UTC
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class NumberType(str, Enum):
    """Valid phone number types."""
    LOCAL = 'local'
    MOBILE = 'mobile'
    TOLLFREE = 'tollfree'

class NumberRecord(BaseModel):
    """Record of a phone number."""
    number: str = Field(..., description="The phone number in E.164 format")
    city: Optional[str] = Field(None, description="City where the number is registered")
    state: Optional[str] = Field(None, description="State/region where the number is registered")
    type: NumberType = Field(..., description="Type of phone number")
    price: Decimal = Field(..., description="Monthly price in USD")
    
    @field_validator('number')
    @classmethod
    def validate_number(cls, v: str) -> str:
        """Validate phone number format."""
        if not v.startswith('+'):
            raise ValueError("Phone number must be in E.164 format (starting with '+')")
        if not v[1:].isdigit():
            raise ValueError("Phone number must contain only digits after '+'")
        return v

class SearchSession(BaseModel):
    """Session data for number search."""
    unique_count: int = Field(0, description="Count of unique numbers found")
    empty_streaks: int = Field(0, description="Consecutive empty result batches")
    batches: int = Field(0, description="Total search batches performed")
    
    @field_validator('unique_count', 'empty_streaks', 'batches')
    @classmethod
    def validate_non_negative(cls, v: int) -> int:
        """Ensure counts are non-negative."""
        if v < 0:
            raise ValueError("Count cannot be negative")
        return v

class UsageStats(BaseModel):
    """Phone number usage statistics."""
    usage: int = Field(..., description="Current usage count")
    cost: Decimal = Field(..., description="Current cost in USD")
    projection: Optional[Decimal] = Field(None, description="Projected monthly cost")
    
    @field_validator('usage')
    @classmethod
    def validate_usage(cls, v: int) -> int:
        """Ensure usage is non-negative."""
        if v < 0:
            raise ValueError("Usage cannot be negative")
        return v
    
    @field_validator('cost', 'projection')
    @classmethod
    def validate_cost(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Ensure costs are non-negative."""
        if v is not None and v < 0:
            raise ValueError("Cost cannot be negative")
        return v

class LogDirection(str, Enum):
    """Direction of communication."""
    INBOUND = 'inbound'
    OUTBOUND = 'outbound'

class LogStatus(str, Enum):
    """Status of the communication."""
    SUCCESS = 'success'
    FAILURE = 'failure'
    PENDING = 'pending'

class LogEntry(BaseModel):
    """Entry in the communication log."""
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the event occurred"
    )
    direction: LogDirection = Field(..., description="Direction of communication")
    status: LogStatus = Field(..., description="Status of the communication")
    details: str = Field(..., description="Additional details about the event")