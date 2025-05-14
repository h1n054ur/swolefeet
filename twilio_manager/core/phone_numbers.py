# File: twilio_manager/core/phone_numbers.py

from typing import List, Dict, Tuple, Optional, Callable
from twilio_manager.services.phone_service import (
    search_available_numbers_api,
    purchase_number_api,
    configure_number_api,
    release_number_api,
    get_active_numbers_api
)

# Country code mapping
COUNTRY_MAP = {
    '+1': 'US',    # USA/Canada
    '1': 'US',     # Handle without plus
    '+44': 'GB',   # UK
    '44': 'GB',    # Handle without plus
    '+61': 'AU',   # Australia
    '61': 'AU',    # Handle without plus
    # Add more mappings as needed
}

def search_available_numbers(
    country_code: str, 
    number_type: str = "local", 
    capabilities: Optional[List[str]] = None, 
    pattern: str = "",
    progress_callback: Optional[Callable[[int], None]] = None
) -> Tuple[List[Dict], str]:
    """
    Search for available phone numbers with pagination and progress tracking.
    
    Args:
        country_code: Country code (e.g., "+1" for US/Canada)
        number_type: Type of number ("local", "tollfree", or "mobile")
        capabilities: List of required capabilities (e.g., ["VOICE", "SMS"])
        pattern: Optional pattern to search for in the number
        progress_callback: Optional callback function to report progress
    
    Returns:
        Tuple of (results list, status message)
    """
    try:
        from twilio_manager.shared.utils.logger import get_logger
        logger = get_logger(__name__)

        # Clean and validate country code
        raw_code = str(country_code).strip()
        # If user passed an ISO code (e.g. "US"), accept as-is
        if raw_code.upper() in set(COUNTRY_MAP.values()):
            country = raw_code.upper()
        else:
            # Attempt dial‐code lookup with or without '+'
            key = raw_code.upper()
            country = COUNTRY_MAP.get(key) or COUNTRY_MAP.get(key.lstrip('+'))

        if not country:
            logger.error(f"Invalid country code: {raw_code}")
            return [], f"Invalid country code: {raw_code}"
            
        logger.debug(f"Mapped country code {country_code} to {country}")
        
        # Default capabilities if none provided
        if capabilities is None:
            capabilities = ["SMS", "VOICE"]
        elif isinstance(capabilities, str):
            capabilities = [capabilities]
            
        logger.debug(f"Using capabilities: {capabilities}")
            
        # Convert capabilities to uppercase and deduplicate
        capabilities = list(set(cap.upper() for cap in capabilities))
        
        # Normalize number type
        number_type = str(number_type).lower().strip()
        if number_type not in ["local", "tollfree", "mobile"]:
            number_type = "local"
            
        # Clean up pattern
        pattern = str(pattern).strip() if pattern else ""
        
        # Call API with normalized parameters (fixed keyword here)
        return search_available_numbers_api(
            country=country,
            number_type=number_type,
            capabilities=capabilities,
            contains=pattern,
            progress_callback=progress_callback
        )

    except Exception as e:
        return [], f"Core layer error: {str(e)}"

def purchase_number(phone_number) -> Tuple[bool, Optional[str]]:
    """Purchase a phone number.
    
    Args:
        phone_number (str): The phone number to purchase
        
    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        success = purchase_number_api(phone_number)
        return success, None
    except Exception as e:
        return False, str(e)

def configure_number(
    sid_or_number, 
    friendly_name=None, 
    voice_url=None, 
    sms_url=None
) -> Tuple[bool, Optional[str]]:
    """Configure a phone number.
    
    Args:
        sid_or_number (str): The phone number or SID to configure
        friendly_name (str, optional): Friendly name for the number
        voice_url (str, optional): URL for voice webhook
        sms_url (str, optional): URL for SMS webhook
        
    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        success = configure_number_api(
            sid_or_number,
            friendly_name=friendly_name,
            voice_url=voice_url,
            sms_url=sms_url
        )
        return success, None
    except Exception as e:
        return False, str(e)

def release_number(sid_or_number) -> Tuple[bool, Optional[str]]:
    """Release a phone number.
    
    Args:
        sid_or_number (str): The phone number or SID to release
        
    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    try:
        success = release_number_api(sid_or_number)
        return success, None
    except Exception as e:
        return False, str(e)

def get_active_numbers() -> Tuple[List[Dict], Optional[str]]:
    """Get all active phone numbers from the account.
    
    Returns:
        Tuple[List[Dict], Optional[str]]: (numbers_list, error_message)
    """
    try:
        numbers = get_active_numbers_api()
        return numbers, None
    except Exception as e:
        return [], str(e)
