from twilio_manager.services.voice_service import (
    make_call_api,
    fetch_call_logs_api
)

def make_call(from_number, to_number, voice_url) -> tuple[bool, str | None]:
    """Make a phone call.
    
    Args:
        from_number (str): Caller phone number
        to_number (str): Recipient phone number
        voice_url (str): URL for voice TwiML
        
    Returns:
        tuple[bool, str | None]: (success, error_message)
    """
    try:
        success = make_call_api(from_number, to_number, voice_url)
        return success, None
    except Exception as e:
        return False, str(e)

def get_call_logs() -> tuple[list, str | None]:
    """Get call logs.
    
    Returns:
        tuple[list, str | None]: (call_logs, error_message)
    """
    try:
        logs = fetch_call_logs_api()
        return logs, None
    except Exception as e:
        return [], str(e)
