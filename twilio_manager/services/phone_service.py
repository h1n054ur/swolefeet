from twilio.rest import Client
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN

client = Client(ACCOUNT_SID, AUTH_TOKEN)

import time
from typing import Dict, List, Set, Tuple, Optional
from twilio.base.exceptions import TwilioRestException

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

def format_phone_number(number, country: str, number_type: str) -> Optional[Dict]:
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
                monthly_rate = PRICE_MAP.get((country, number_type), 1.15)
        except (ValueError, TypeError):
            monthly_rate = PRICE_MAP.get((country, number_type), 1.15)

        return {
            "phoneNumber": getattr(number, 'phone_number', '—'),
            "friendlyName": getattr(number, 'friendly_name', '') or getattr(number, 'phone_number', '—'),
            "region": getattr(number, 'locality', '') or getattr(number, 'region', '') or "—",
            "capabilities": caps_dict,
            "monthlyPrice": monthly_rate
        }
    except Exception:
        return None

def search_available_numbers_api(country: str, type: str, capabilities: List[str], contains: str = "", 
                               progress_callback=None) -> Tuple[List[Dict], str]:
    """
    Search for available phone numbers with pagination and rate limiting.
    
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
        # Set up search parameters
        kwargs = {
            "limit": 100  # Maximum allowed by Twilio
        }
        
        # Add capability filters
        if "SMS" in capabilities:
            kwargs["sms_enabled"] = True
        if "VOICE" in capabilities:
            kwargs["voice_enabled"] = True
        if "MMS" in capabilities:
            kwargs["mms_enabled"] = True
            
        # Add pattern if provided
        if contains:
            kwargs["contains"] = contains
            
        # Add area code if it's a valid US area code pattern
        if country == "US" and contains and contains.isdigit() and len(contains) == 3:
            kwargs["area_code"] = contains
            kwargs.pop("contains", None)

        # Get the appropriate subresource based on type
        type_map = {
            "local": client.available_phone_numbers(country).local,
            "tollfree": client.available_phone_numbers(country).toll_free,
            "mobile": client.available_phone_numbers(country).mobile
        }
        
        number_type = type_map.get(type.lower())
        if not number_type:
            return [], "Invalid number type specified"

        # Initialize tracking variables
        results = []
        seen_numbers: Set[str] = set()
        consecutive_empty = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                # Query the API with page_size
                kwargs['page_size'] = 100  # Maximum allowed by Twilio
                
                # Get the first page of results
                page = number_type.list(**kwargs)
                
                while True:
                    # Process current page
                    new_numbers = 0
                    for n in page:
                        phone_number = getattr(n, 'phone_number', None)
                        if not phone_number or phone_number in seen_numbers:
                            continue
                            
                        formatted = format_phone_number(n, country, type.lower())
                        if formatted:
                            results.append(formatted)
                            seen_numbers.add(phone_number)
                            new_numbers += 1
                            
                            # Stop if we've reached 500 numbers
                            if len(results) >= 500:
                                break
                    
                    # Update progress if callback provided
                    if progress_callback:
                        progress_callback(len(results))
                    
                    # Check if we found any new numbers
                    if new_numbers == 0:
                        consecutive_empty += 1
                    else:
                        consecutive_empty = 0
                    
                    # Stop conditions
                    if len(results) >= 500 or consecutive_empty >= 2:
                        break
                        
                    # Check if there are more pages
                    if not page.next_page_url:
                        break
                        
                    # Add delay for rate limiting
                    time.sleep(1)
                    
                    # Get next page
                    page = page.next_page()
                
                break  # Break from retry loop
                
            except TwilioRestException as e:
                if e.status == 429:  # Rate limit error
                    retry_count += 1
                    time.sleep(2 ** retry_count)  # Exponential backoff
                else:
                    return results, f"Twilio API error: {str(e)}"
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    return results, f"Error after {max_retries} retries: {str(e)}"
                time.sleep(2 ** retry_count)
        
        # Determine status message
        if len(results) >= 500:
            status = "Found maximum number of results (500)"
        elif consecutive_empty >= 2:
            status = "Search completed (no more results available)"
        else:
            status = "Search completed successfully"
        
        return results, status

    except Exception as e:
        return [], f"Unexpected error: {str(e)}"


def purchase_number_api(phone_number):
    number = client.incoming_phone_numbers.create(phone_number=phone_number)
    return bool(number and number.sid)


def configure_number_api(sid_or_number, friendly_name=None, voice_url=None, sms_url=None):
    for num in client.incoming_phone_numbers.list():
        if sid_or_number in (num.sid, num.phone_number):
            update_kwargs = {}
            if friendly_name: update_kwargs["friendly_name"] = friendly_name
            if voice_url: update_kwargs["voice_url"] = voice_url
            if sms_url: update_kwargs["sms_url"] = sms_url
            updated = client.incoming_phone_numbers(num.sid).update(**update_kwargs)
            return bool(updated)
    return False


def release_number_api(sid_or_number):
    for num in client.incoming_phone_numbers.list():
        if sid_or_number in (num.sid, num.phone_number):
            return client.incoming_phone_numbers(num.sid).delete()
    return False


def get_active_numbers_api():
    """Fetch all active phone numbers from the Twilio account."""
    numbers = client.incoming_phone_numbers.list()
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
