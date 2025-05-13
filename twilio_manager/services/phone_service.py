import time
import random
import requests
from typing import Dict, List, Set, Tuple, Optional, Callable
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN
from twilio_manager.shared.utils.logger import get_logger
from urllib.parse import urlparse, parse_qs

logger = get_logger(__name__)

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
        """Initialize the phone service with Twilio client."""
        try:
            self.client = Client(ACCOUNT_SID, AUTH_TOKEN)
            logger.info("PhoneService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PhoneService: {str(e)}")
            raise

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
        except Exception as e:
            logger.error(f"Error formatting phone number: {str(e)}", exc_info=True)
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
        except Exception as e:
            logger.error(f"Error formatting phone number object: {str(e)}", exc_info=True)
            return None

    def _search_available_numbers_api(self, country: str, type: str, capabilities: List[str], contains: str = "", 
                               progress_callback: Optional[Callable[[int], None]] = None) -> Tuple[List[Dict], str]:
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
                if "SMS" in capabilities:
                    params["SmsEnabled"] = "true"
                if "VOICE" in capabilities:
                    params["VoiceEnabled"] = "true"
                if "MMS" in capabilities:
                    params["MmsEnabled"] = "true"
                    
            # Add pattern if provided
            if contains:
                if country == "US" and contains.isdigit() and len(contains) == 3:
                    params["AreaCode"] = contains
                else:
                    params["Contains"] = contains

            # Initialize tracking variables
            results = []
            seen_numbers: Set[str] = set()
            consecutive_no_unique = 0
            max_retries = 5  # Increased max retries
            retry_count = 0
            page = 1
            
            while len(results) < 500 and consecutive_no_unique < 3:  # Increased threshold
                try:
                    # Add page parameter for pagination
                    params['Page'] = page
                    params['PageSize'] = 100  # Increased page size
                    
                    # Make request with basic auth and proper headers
                    headers = {
                        'Accept': 'application/json',
                        'User-Agent': 'TwilioManager/1.0'
                    }
                    
                    response = requests.get(
                        base_url,
                        auth=(ACCOUNT_SID, AUTH_TOKEN),
                        params=params,
                        headers=headers,
                        timeout=45  # Increased timeout
                    )
                    
                    # Handle rate limiting explicitly
                    if response.status_code == 429:
                        retry_after = int(response.headers.get('Retry-After', 30))
                        logger.warning(f"Rate limit hit, waiting {retry_after} seconds")
                        time.sleep(retry_after)
                        continue
                        
                    response.raise_for_status()
                    
                    # Parse response
                    data = response.json()
                    new_unique = 0
                    
                    # Process numbers from response
                    numbers = data.get('available_phone_numbers', [])
                    if not numbers:
                        consecutive_no_unique += 1
                        if consecutive_no_unique >= 3:
                            break
                        page += 1
                        continue
                    
                    for number in numbers:
                        phone_number = number.get('phone_number')
                        if not phone_number or phone_number in seen_numbers:
                            continue
                        
                        formatted = self._format_phone_number_dict(number, country, type.lower())
                        if formatted:
                            results.append(formatted)
                            seen_numbers.add(phone_number)
                            new_unique += 1
                            
                            # Update progress more frequently
                            if progress_callback and new_unique % 10 == 0:
                                progress_callback(len(results))
                            
                            if len(results) >= 500:
                                break
                    
                    # Final progress update for this page
                    if progress_callback:
                        progress_callback(len(results))
                    
                    # Check if we found new unique numbers
                    if new_unique == 0:
                        consecutive_no_unique += 1
                    else:
                        consecutive_no_unique = 0
                    
                    # Move to next page
                    page += 1
                    
                    # Adaptive rate limiting
                    remaining = int(response.headers.get('X-RateLimit-Remaining', 100))
                    if remaining < 10:
                        time.sleep(2)
                    else:
                        time.sleep(0.5)
                    
                except requests.exceptions.RequestException as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        logger.error(f"Search failed after {max_retries} retries: {str(e)}")
                        return results, f"Error after {max_retries} retries: {str(e)}"
                    
                    # Enhanced exponential backoff
                    wait_time = min(30, 2 ** retry_count + random.uniform(0, 1))
                    logger.warning(f"Request failed, retrying in {wait_time:.1f} seconds")
                    time.sleep(wait_time)
                    continue
                except Exception as e:
                    logger.error(f"API error: {str(e)}", exc_info=True)
                    return results, f"API error: {str(e)}"
            
            # Determine status message
            if len(results) >= 500:
                status = f"Found maximum number of results (500)"
            elif consecutive_no_unique >= 3:
                status = f"Search completed (found {len(results)} numbers)"
            else:
                status = f"Search completed successfully (found {len(results)} numbers)"
            
            logger.info(f"Search completed: {status}")
            return results, status

        except Exception as e:
            logger.error(f"Unexpected error in search: {str(e)}", exc_info=True)
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
            success = bool(number and number.sid)
            if success:
                logger.info(f"Successfully purchased number: {phone_number}")
            else:
                logger.warning(f"Failed to purchase number: {phone_number}")
            return success
        except TwilioRestException as e:
            logger.error(f"Twilio error purchasing number {phone_number}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error purchasing number {phone_number}: {str(e)}", exc_info=True)
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
                    success = bool(updated)
                    if success:
                        logger.info(f"Successfully configured number: {sid_or_number}")
                    else:
                        logger.warning(f"Failed to configure number: {sid_or_number}")
                    return success
            logger.warning(f"Number not found: {sid_or_number}")
            return False
        except TwilioRestException as e:
            logger.error(f"Twilio error configuring number {sid_or_number}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error configuring number {sid_or_number}: {str(e)}", exc_info=True)
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
                    success = bool(self.client.incoming_phone_numbers(num.sid).delete())
                    if success:
                        logger.info(f"Successfully released number: {sid_or_number}")
                    else:
                        logger.warning(f"Failed to release number: {sid_or_number}")
                    return success
            logger.warning(f"Number not found: {sid_or_number}")
            return False
        except TwilioRestException as e:
            logger.error(f"Twilio error releasing number {sid_or_number}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error releasing number {sid_or_number}: {str(e)}", exc_info=True)
            return False

    def get_active_numbers(self) -> List[Dict]:
        """Get all active phone numbers.
        
        Returns:
            List of active phone numbers with their details
        """
        try:
            numbers = self.client.incoming_phone_numbers.list()
            result = [
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
            logger.info(f"Retrieved {len(result)} active numbers")
            return result
        except TwilioRestException as e:
            logger.error(f"Twilio error getting active numbers: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting active numbers: {str(e)}", exc_info=True)
            return []