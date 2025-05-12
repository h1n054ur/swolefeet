from twilio.rest import Client
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def search_available_numbers_api(country, type, capabilities, contains=""):
    """
    Search for available phone numbers.
    
    Args:
        country: Country code (e.g., "US")
        type: Type of number ("local", "tollfree", or "mobile")
        capabilities: List of required capabilities (e.g., ["SMS", "VOICE"])
        contains: Optional pattern to search for in the number
    """
    try:
        print(f"[DEBUG] Searching for numbers with params:")
        print(f"  Country: {country}")
        print(f"  Type: {type}")
        print(f"  Capabilities: {capabilities}")
        print(f"  Pattern: {contains}")

        # Set up search parameters
        kwargs = {}
        
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
            # Remove contains to avoid conflict
            kwargs.pop("contains", None)

        print(f"[DEBUG] Search parameters: {kwargs}")

        # Get the appropriate subresource based on type
        type_map = {
            "local": client.available_phone_numbers(country).local,
            "tollfree": client.available_phone_numbers(country).toll_free,
            "mobile": client.available_phone_numbers(country).mobile
        }
        
        number_type = type_map.get(type.lower())
        if not number_type:
            print(f"[DEBUG] Invalid number type: {type}")
            return []

        print(f"[DEBUG] Using number type: {type.lower()}")

        # Fetch numbers with limit to ensure we get some results
        numbers = number_type.list(limit=20, **kwargs)
        
        # Convert to list to check length
        numbers = list(numbers)
        print(f"[DEBUG] Found {len(numbers)} numbers")

        # Format results
        results = []
        for n in numbers:
            try:
                # Get capabilities safely
                caps = getattr(n, 'capabilities', {})
                if isinstance(caps, (list, tuple)):
                    # Handle case where capabilities might be a list
                    caps_dict = {
                        "voice": "voice" in caps,
                        "sms": "sms" in caps,
                        "mms": "mms" in caps
                    }
                else:
                    # Handle case where capabilities is a dict
                    caps_dict = {
                        "voice": caps.get("voice", False),
                        "sms": caps.get("sms", False),
                        "mms": caps.get("mms", False)
                    }

                # Build result dict with safe attribute access
                result = {
                    "phoneNumber": getattr(n, 'phone_number', '—'),
                    "friendlyName": getattr(n, 'friendly_name', '') or getattr(n, 'phone_number', '—'),
                    "region": getattr(n, 'locality', '') or getattr(n, 'region', '') or "—",
                    "capabilities": caps_dict
                }

                # Handle monthly rate
                try:
                    result["monthlyPrice"] = float(getattr(n, 'monthly_rate', 0) or 0)
                except (ValueError, TypeError):
                    result["monthlyPrice"] = 0.0

                results.append(result)
                
            except Exception as e:
                print(f"[DEBUG] Error formatting number {n}: {str(e)}")
                continue
        
        print(f"[DEBUG] Formatted {len(results)} results")
        return results

    except Exception as e:
        print(f"[service] Search error: {str(e)}")
        import traceback
        print(f"[DEBUG] Full error: {traceback.format_exc()}")
        return []


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
