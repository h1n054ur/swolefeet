import time
import requests
from typing import Dict, List, Set, Tuple, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN
from urllib.parse import urlparse, parse_qs

# Create singleton instance
_phone_service = None

def get_phone_service():
    global _phone_service
    if _phone_service is None:
        _phone_service = PhoneService()
    return _phone_service

# Export API functions that match the old interface
def search_available_numbers_api(*args, **kwargs):
    return get_phone_service()._search_available_numbers_api(*args, **kwargs)

def purchase_number_api(phone_number):
    return get_phone_service().purchase_number(phone_number)

def configure_number_api(sid_or_number, friendly_name=None, voice_url=None, sms_url=None):
    return get_phone_service().configure_number(sid_or_number, friendly_name, voice_url, sms_url)

def release_number_api(sid_or_number):
    return get_phone_service().release_number(sid_or_number)

def get_active_numbers_api():
    return get_phone_service().get_active_numbers()

class PhoneService:
    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Price mapping for different number types and countries
    PRICE_MAP = {
        ("US", "local"): 1.15,        # US local numbers
        ("US", "tollfree"): 2.15,     # US toll-free numbers
        ("US", "mobile"): 1.15,       # US mobile numbers
        ("GB", "local"): 1.15,        # UK local numbers
        ("GB", "mobile"): 1.15,       # UK mobile numbers
        ("GB", "tollfree"): 2.15,     # UK toll-free numbers
        ("AU", "local"): 3.00,        # AU local numbers
        ("AU", "mobile"): 6.50,       # AU mobile numbers
        ("AU", "tollfree"): 16.00,    # AU toll-free numbers
        ("CA", "local"): 1.15,        # CA local numbers
        ("CA", "tollfree"): 2.15      # CA toll-free numbers
    }

    def _format_phone_number_dict(self, number_dict: Dict, country: str, number_type: str) -> Optional[Dict]:
        """Format a phone number dictionary from the REST API response."""
        try:
            # Get capabilities safely
            caps = number_dict.get('capabilities', {})
            if isinstance(caps, (list, tuple)):
                caps_dict = {
                    "voice": "voice" in caps,
                    "sms": "sms" in caps,
                    "mms": "mms" in caps
                }
            else:
                caps_dict = {
                    "voice": caps.get("voice", False),
                    "sms": caps.get("sms", False),
                    "mms": caps.get("mms", False)
                }

            # Get monthly price from API or use default from price map
            try:
                monthly_rate = float(number_dict.get('monthly_rate', 0))
                if monthly_rate == 0:
                    monthly_rate = self.PRICE_MAP.get((country, number_type), 1.15)
            except (ValueError, TypeError):
                monthly_rate = self.PRICE_MAP.get((country, number_type), 1.15)

            return {
                "phoneNumber": number_dict.get('phone_number', '—'),
                "friendlyName": number_dict.get('friendly_name', '') or number_dict.get('phone_number', '—'),
                "region": number_dict.get('locality', '') or number_dict.get('region', '') or "—",
                "capabilities": caps_dict,
                "monthlyPrice": monthly_rate
            }
        except Exception:
            return None

    def _format_phone_number(self, number, country: str, number_type: str) -> Optional[Dict]:
        """Format a phone number object into our standard dictionary format."""
        try:
            # Get capabilities safely
            caps = getattr(number, 'capabilities', {})
            if isinstance(caps, (list, tuple)):
                caps_dict = {
                    "voice": "voice" in caps,
                    "sms": "sms" in caps,
                    "mms": "mms" in caps
                }
            else:
                caps_dict = {
                    "voice": caps.get("voice", False),
                    "sms": caps.get("sms", False),
                    "mms": caps.get("mms", False)
                }

            # Get monthly price from API or use default from price map
            try:
                monthly_rate = float(getattr(number, 'monthly_rate', None) or 0)
                if monthly_rate == 0:
                    monthly_rate = self.PRICE_MAP.get((country, number_type), 1.15)
            except (ValueError, TypeError):
                monthly_rate = self.PRICE_MAP.get((country, number_type), 1.15)

            return {
                "phoneNumber": getattr(number, 'phone_number', '—'),
                "friendlyName": getattr(number, 'friendly_name', '') or getattr(number, 'phone_number', '—'),
                "region": getattr(number, 'locality', '') or getattr(number, 'region', '') or "—",
                "capabilities": caps_dict,
                "monthlyPrice": monthly_rate
            }
        except Exception:
            return None

    def search_numbers(self, country_code: str, number_type: str, capabilities: List[str], pattern: str = "") -> List[Dict]:
        """Search for available phone numbers.
        
        Args:
            country_code: Country code (e.g., "US")
            number_type: Type of number ("local", "tollfree", or "mobile")
            capabilities: List of required capabilities (e.g., ["SMS", "VOICE"])
            pattern: Optional pattern to search for in the number
            
        Returns:
            List of available phone numbers
        """
        results, _ = self._search_available_numbers_api(country_code, number_type, capabilities, pattern)
        return results

    # Valid country codes and their supported number types
    SUPPORTED_COUNTRIES = {
        "US": ["local", "tollfree", "mobile"],
        "GB": ["local", "tollfree", "mobile"],
        "CA": ["local", "tollfree"],
        "AU": ["local", "tollfree", "mobile"]
    }

    def _search_available_numbers_api(self, country: str, type: str, capabilities: List[str], contains: str = "", 
                               progress_callback=None) -> Tuple[List[Dict], str]:
        """
        Search for available phone numbers using direct HTTP requests with pagination.
        
        Args:
            country: Country code (e.g., "US")
            type: Type of number ("local", "tollfree", or "mobile")
            capabilities: List of required capabilities (e.g., ["SMS", "VOICE"])
            contains: Optional pattern to search for in the number
            progress_callback: Optional callback function to report progress
        
        Returns:
            Tuple of (results list, status message)
        """
        from twilio_manager.shared.utils.logger import get_logger
        logger = get_logger(__name__)
        
        # Validate country code and number type
        country = country.upper()
        type = type.lower()
        
        if country not in self.SUPPORTED_COUNTRIES:
            return [], f"Unsupported country code: {country}"
            
        if type not in self.SUPPORTED_COUNTRIES[country]:
            return [], f"Number type '{type}' not supported for country {country}"
        try:
            # Map number types to API endpoints
            type_map = {
                "local": "Local",
                "tollfree": "TollFree",
                "mobile": "Mobile"
            }
            
            number_type = type_map.get(type.lower())
            if not number_type:
                return [], "Invalid number type specified"
                
            # Base URL for Twilio API
            base_url = f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/AvailablePhoneNumbers/{country}/{number_type}.json"
            
            # Set up initial parameters with capability filters
            params = {}
            if capabilities:
                # Convert capabilities to uppercase and handle variations
                caps = [cap.upper().strip() for cap in capabilities]
                capability_map = {
                    "SMS": "SmsEnabled",
                    "VOICE": "VoiceEnabled",
                    "MMS": "MmsEnabled",
                    "MESSAGING": "SmsEnabled",  # Handle alternative names
                    "CALL": "VoiceEnabled",
                    "TEXT": "SmsEnabled"
                }
                for cap in caps:
                    if cap in capability_map:
                        params[capability_map[cap]] = "true"
                    
            # Add pattern if provided
            if contains:
                contains = contains.strip()
                # Handle US area codes (3 digits)
                if country == "US" and contains.isdigit():
                    if len(contains) == 3:
                        params["AreaCode"] = contains
                    elif len(contains) > 3:
                        # If more than 3 digits, use Contains for full number search
                        params["Contains"] = contains
                    else:
                        # For 1-2 digits, search in both area code and number
                        params["Contains"] = contains
                else:
                    # For non-US or non-digit patterns
                    params["Contains"] = contains
                
                logger.debug(f"Pattern parameters: {params}")

            # Initialize tracking variables
            results = []
            seen_numbers: Set[str] = set()
            consecutive_no_unique = 0
            max_retries = 3
            retry_count = 0
            
            while len(results) < 500 and consecutive_no_unique < 2:
                try:
                    # Log request parameters
                    from twilio_manager.shared.utils.logger import get_logger
                    logger = get_logger(__name__)
                    logger.debug(f"Searching numbers with params: {params}")
                    logger.debug(f"Request URL: {base_url}")
                    
                    # Make request with basic auth
                    response = requests.get(
                        base_url,
                        auth=(ACCOUNT_SID, AUTH_TOKEN),
                        params=params,
                        timeout=30
                    )
                    
                    # Log response status and content
                    logger.debug(f"Response status: {response.status_code}")
                    logger.debug(f"Response content: {response.text[:500]}...")  # Log first 500 chars
                    
                    response.raise_for_status()
                    
                    # Parse response
                    data = response.json()
                    new_unique = 0
                    
                    # Process numbers from response
                    numbers = data.get('available_phone_numbers', [])
                    
                    for number in numbers:
                        phone_number = number.get('phone_number')
                        if not phone_number or phone_number in seen_numbers:
                            continue
                        
                        formatted = self._format_phone_number_dict(number, country, type.lower())
                        if formatted:
                            results.append(formatted)
                            seen_numbers.add(phone_number)
                            new_unique += 1
                            
                            if len(results) >= 500:
                                break
                    
                    # Update progress
                    if progress_callback:
                        progress_callback(len(results))
                    
                    # Check if we found new unique numbers
                    if new_unique == 0:
                        consecutive_no_unique += 1
                    else:
                        consecutive_no_unique = 0
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except requests.exceptions.RequestException as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        return results, f"Error after {max_retries} retries: {str(e)}"
                        
                    # Handle rate limits with exponential backoff
                    if getattr(e.response, 'status_code', None) == 429:
                        time.sleep(2 ** retry_count)
                    else:
                        time.sleep(1)
                    continue
            
            # Determine status message
            if len(results) >= 500:
                status = "Found maximum number of results (500)"
            elif consecutive_no_unique >= 2:
                status = "Search completed (no more results available)"
            else:
                status = "Search completed successfully"
            
            return results, status

        except Exception as e:
            return [], f"Unexpected error: {str(e)}"


    def purchase_number(self, phone_number: str) -> bool:
        """Purchase a phone number.
        
        Args:
            phone_number: The phone number to purchase
            
        Returns:
            bool: True if purchase was successful
        """
        try:
            number = self.client.incoming_phone_numbers.create(phone_number=phone_number)
            return bool(number and number.sid)
        except TwilioRestException:
            return False

    def configure_number(self, sid_or_number: str, friendly_name: str = None, voice_url: str = None, sms_url: str = None) -> bool:
        """Configure a phone number's settings.
        
        Args:
            sid_or_number: The phone number or SID to configure
            friendly_name: Optional friendly name to set
            voice_url: Optional voice URL to set
            sms_url: Optional SMS URL to set
            
        Returns:
            bool: True if configuration was successful
        """
        try:
            for num in self.client.incoming_phone_numbers.list():
                if sid_or_number in (num.sid, num.phone_number):
                    update_kwargs = {}
                    if friendly_name: update_kwargs["friendly_name"] = friendly_name
                    if voice_url: update_kwargs["voice_url"] = voice_url
                    if sms_url: update_kwargs["sms_url"] = sms_url
                    updated = self.client.incoming_phone_numbers(num.sid).update(**update_kwargs)
                    return bool(updated)
            return False
        except TwilioRestException:
            return False

    def release_number(self, sid_or_number: str) -> bool:
        """Release a phone number.
        
        Args:
            sid_or_number: The phone number or SID to release
            
        Returns:
            bool: True if release was successful
        """
        try:
            for num in self.client.incoming_phone_numbers.list():
                if sid_or_number in (num.sid, num.phone_number):
                    return bool(self.client.incoming_phone_numbers(num.sid).delete())
            return False
        except TwilioRestException:
            return False

    def get_active_numbers(self) -> List[Dict]:
        """Get all active phone numbers.
        
        Returns:
            List of active phone numbers with their details
        """
        try:
            numbers = self.client.incoming_phone_numbers.list()
            return [
                {
                    "sid": n.sid,
                    "phoneNumber": n.phone_number,
                    "friendlyName": n.friendly_name or n.phone_number,
                    "capabilities": {
                        "voice": n.capabilities.get("voice", False),
                        "sms": n.capabilities.get("sms", False),
                        "mms": n.capabilities.get("mms", False)
                    },
                    "voiceUrl": n.voice_url,
                    "smsUrl": n.sms_url
                } for n in numbers
            ]
        except TwilioRestException:
            return []
