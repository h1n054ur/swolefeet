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
        # Set up search parameters
        kwargs = {
            "sms_enabled": "SMS" in capabilities,
            "voice_enabled": "VOICE" in capabilities,
            "mms_enabled": "MMS" in capabilities
        }
        if contains:
            kwargs["contains"] = contains

        # Get the appropriate subresource based on type
        number_type = {
            "local": lambda: client.available_phone_numbers(country).local,
            "tollfree": lambda: client.available_phone_numbers(country).toll_free,
            "mobile": lambda: client.available_phone_numbers(country).mobile
        }.get(type.lower(), lambda: client.available_phone_numbers(country).local)()

        # Fetch numbers
        numbers = number_type.list(**kwargs)

        # Format results
        return [
            {
                "sid": n.sid,
                "phoneNumber": n.phone_number,
                "friendlyName": n.friendly_name or n.phone_number,
                "region": n.locality or n.region or "—",
                "capabilities": {
                    "voice": n.capabilities.get("voice", False),
                    "sms": n.capabilities.get("sms", False),
                    "mms": n.capabilities.get("mms", False)
                },
                "monthlyPrice": n.monthly_rate or 0
            } for n in numbers
        ]
    except Exception as e:
        print(f"[service] Search error: {e}")
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
