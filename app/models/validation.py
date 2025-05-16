"""Validation utilities for Twilio Manager CLI."""

import re
from typing import Set
from .country_data import COUNTRY_DATA

def is_valid_country(country: str) -> bool:
    """Check if a country code is valid.
    
    Args:
        country: ISO country code to validate
        
    Returns:
        True if country code is valid, False otherwise
    """
    return country in COUNTRY_DATA

def is_valid_region(country: str, region: str) -> bool:
    """Check if a region is valid for a country.
    
    Args:
        country: ISO country code
        region: Region name to validate
        
    Returns:
        True if region is valid for the country, False otherwise
    """
    if not is_valid_country(country):
        return False
    return region in COUNTRY_DATA[country]['regions']

def is_valid_number_type(country: str, number_type: str) -> bool:
    """Check if a number type is valid for a country.
    
    Args:
        country: ISO country code
        number_type: Number type to validate
        
    Returns:
        True if number type is valid for the country, False otherwise
    """
    if not is_valid_country(country):
        return False
    return number_type in COUNTRY_DATA[country]['number_types']

def is_valid_area_code(country: str, area_code: int) -> bool:
    """Check if an area code is valid for a country.
    
    Args:
        country: ISO country code
        area_code: Area code to validate
        
    Returns:
        True if area code is valid for the country, False otherwise
    """
    if not is_valid_country(country):
        return False
    
    for region in COUNTRY_DATA[country]['regions'].values():
        if area_code in region['area_codes']:
            return True
    return False

def get_valid_capabilities() -> Set[str]:
    """Get the set of valid Twilio number capabilities.
    
    Returns:
        Set of valid capability strings
    """
    return {
        'voice',
        'SMS',
        'MMS',
        'fax',
        'carrier_lookup',
        'caller_id_lookup'
    }

def is_valid_capability_set(capabilities: Set[str]) -> bool:
    """Check if a set of capabilities is valid.
    
    Args:
        capabilities: Set of capabilities to validate
        
    Returns:
        True if all capabilities are valid, False otherwise
    """
    valid_caps = get_valid_capabilities()
    return all(cap in valid_caps for cap in capabilities)

def is_valid_e164(number: str) -> bool:
    """Check if a phone number is in valid E.164 format.
    
    Args:
        number: Phone number to validate
        
    Returns:
        True if number is in valid E.164 format, False otherwise
    """
    pattern = r'^\+[1-9]\d{1,14}$'
    return bool(re.match(pattern, number))

def normalize_number(number: str) -> str:
    """Normalize a phone number to E.164 format.
    
    Args:
        number: Phone number to normalize
        
    Returns:
        Normalized phone number in E.164 format
        
    Raises:
        ValueError: If number cannot be normalized
    """
    # Remove all non-digit characters except leading +
    digits = ''.join(c for c in number if c.isdigit() or c == '+')
    
    # Add + if missing
    if not digits.startswith('+'):
        # For US/Canada numbers, add +1
        if len(digits) == 10:
            digits = '+1' + digits
        else:
            digits = '+' + digits
    
    if not is_valid_e164(digits):
        raise ValueError(
            f"Cannot normalize '{number}' to E.164 format"
        )
    
    return digits