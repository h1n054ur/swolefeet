"""Data models for account-related information."""

from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class UsageStats:
    """Statistics about account usage and costs."""
    usage: Dict[str, Dict]  # Category -> {usage, units, cost}
    cost: float  # Total cost for the period
    projection: float  # Projected monthly cost

@dataclass
class BillingInfo:
    """Account billing information."""
    balance: float
    currency: str
    last_month_charges: float
    last_month_usage: float
    last_month_fees: float

@dataclass
class AccountConfig:
    """Account configuration settings."""
    account_sid: str
    auth_token: str
    subaccount_sid: Optional[str] = None
    friendly_name: Optional[str] = None
    status: str = "active"
