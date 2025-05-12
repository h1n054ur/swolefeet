import time
import requests
from typing import Dict, List, Set, Tuple, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN
from urllib.parse import urlparse, parse_qs

client = Client(ACCOUNT_SID, AUTH_TOKEN)

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

def format_phone_number_dict(number_dict: Dict, country: str, number_type: str) -> Optional[Dict]:
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
                monthly_rate = PRICE_MAP.get((country, number_type), 1.15)
        except (ValueError, TypeError):
            monthly_rate = PRICE_MAP.get((country, number_type), 1.15)

        return {
            "phoneNumber": number_dict.get('phone_number', '—'),
            "friendlyName": number_dict.get('friendly_name', '') or number_dict.get('phone_number', '—'),
            "region": number_dict.get('locality', '') or number_dict.get('region', '') or "—",
            "capabilities": caps_dict,
            "monthlyPrice": monthly_rate
        }
    except Exception:
        return None

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
        
        # Set up initial parameters
        params = {
            'PageSize': 100,  # Maximum allowed per page
        }
        
        # Add capability filters
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
        max_retries = 3
        retry_count = 0
        page_token = None
        page = 1
        
        while len(results) < 500 and consecutive_no_unique < 2:
            try:
                # Add page token if we have one
                if page_token:
                    params['PageToken'] = page_token
                
                # Debug logging
                print(f"\nQuerying page {page}...")
                
                # Make request with basic auth
                response = requests.get(
                    base_url,
                    auth=(ACCOUNT_SID, AUTH_TOKEN),
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                
                # Parse response
                data = response.json()
                new_unique = 0
                
                # Process numbers from this page
                page_numbers = data.get('available_phone_numbers', [])
                print(f"Found {len(page_numbers)} numbers in response")
                
                for number in page_numbers:
                    phone_number = number.get('phone_number')
                    if not phone_number or phone_number in seen_numbers:
                        continue
                    
                    formatted = format_phone_number_dict(number, country, type.lower())
                    if formatted:
                        results.append(formatted)
                        seen_numbers.add(phone_number)
                        new_unique += 1
                        
                        if len(results) >= 500:
                            break
                
                # Update progress
                if progress_callback:
                    progress_callback(len(results))
                
                print(f"Added {new_unique} unique numbers")
                
                # Check if we found new unique numbers
                if new_unique == 0:
                    consecutive_no_unique += 1
                    print(f"No new unique numbers found. Attempt {consecutive_no_unique}/2")
                else:
                    consecutive_no_unique = 0
                    
                page += 1
                
                # Get next page token from URI
                next_page_uri = data.get('next_page_uri')
                if not next_page_uri:
                    break
                    
                # Parse next page token from URI
                parsed = urlparse(next_page_uri)
                query_params = parse_qs(parsed.query)
                page_token = query_params.get('PageToken', [None])[0]
                
                if not page_token:
                    break
                
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
