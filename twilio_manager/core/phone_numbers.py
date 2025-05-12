from twilio_manager.services.phone_service import (
    search_available_numbers_api,
    purchase_number_api,
    configure_number_api,
    release_number_api
)

def search_available_numbers(country, number_type, capabilities, pattern=""):
    try:
        return search_available_numbers_api(
            country=country,
            type=number_type,
            capabilities=capabilities,
            contains=pattern
        )
    except Exception as e:
        print(f"[core] Search error: {e}")
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
