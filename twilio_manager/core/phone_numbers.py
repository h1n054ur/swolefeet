from twilio_manager.services.phone_service import (
    search_available_numbers_api,
    purchase_number_api,
    configure_number_api,
    release_number_api,
    get_active_numbers_api
)

def search_available_numbers(country_code, number_type="local", capabilities=None, pattern=""):
    """
    Search for available phone numbers.
    
    Args:
        country_code: Country code (e.g., "+1" for US/Canada)
        number_type: Type of number ("local", "tollfree", or "mobile")
        capabilities: List of required capabilities (e.g., ["VOICE", "SMS"])
        pattern: Optional pattern to search for in the number
    """
    try:
        print(f"[DEBUG] Core layer received:")
        print(f"  Country code: {country_code}")
        print(f"  Number type: {number_type}")
        print(f"  Capabilities: {capabilities}")
        print(f"  Pattern: {pattern}")

        # Convert E.164 prefix to ISO country code
        country_map = {
            '+1': 'US',    # USA/Canada
            '1': 'US',     # Handle without plus
            '+44': 'GB',   # UK
            '44': 'GB',    # Handle without plus
            '+61': 'AU',   # Australia
            '61': 'AU',    # Handle without plus
            # Add more mappings as needed
        }
        
        # Get ISO country code, default to US if not found
        country = country_map.get(country_code, 'US')
        print(f"[DEBUG] Mapped country code {country_code} to {country}")
        
        # Default capabilities if none provided
        if capabilities is None:
            capabilities = ["SMS", "VOICE"]
        elif isinstance(capabilities, str):
            capabilities = [capabilities]
            
        # Convert capabilities to uppercase and deduplicate
        capabilities = list(set(cap.upper() for cap in capabilities))
        print(f"[DEBUG] Normalized capabilities: {capabilities}")
        
        # Normalize number type
        number_type = str(number_type).lower().strip()
        if number_type not in ["local", "tollfree", "mobile"]:
            print(f"[DEBUG] Invalid number type {number_type}, defaulting to local")
            number_type = "local"
            
        # Clean up pattern
        pattern = str(pattern).strip() if pattern else ""
        
        # Call API with normalized parameters
        results = search_available_numbers_api(
            country=country,
            type=number_type,
            capabilities=capabilities,
            contains=pattern
        )
        
        print(f"[DEBUG] Core layer received {len(results)} results")
        return results

    except Exception as e:
        print(f"[core] Search error: {str(e)}")
        import traceback
        print(f"[DEBUG] Full error: {traceback.format_exc()}")
        return []

def purchase_number(phone_number):
    try:
        return purchase_number_api(phone_number)
    except Exception as e:
        print(f"[core] Purchase error: {e}")
        return False

def configure_number(sid_or_number, friendly_name=None, voice_url=None, sms_url=None):
    try:
        return configure_number_api(
            sid_or_number,
            friendly_name=friendly_name,
            voice_url=voice_url,
            sms_url=sms_url
        )
    except Exception as e:
        print(f"[core] Configure error: {e}")
        return False

def release_number(sid_or_number):
    try:
        return release_number_api(sid_or_number)
    except Exception as e:
        print(f"[core] Release error: {e}")
        return False


def get_active_numbers():
    """Get all active phone numbers from the account."""
    try:
        return get_active_numbers_api()
    except Exception as e:
        print(f"[core] Get active numbers error: {e}")
        return []
