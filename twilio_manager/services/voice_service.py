from twilio.rest import Client
from twilio_manager.shared.config import ACCOUNT_SID, AUTH_TOKEN

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def make_call_api(from_number, to_number, voice_url) -> tuple[bool, str | None]:
    """Make a phone call using Twilio API.
    
    Args:
        from_number (str): Caller phone number
        to_number (str): Recipient phone number
        voice_url (str): URL for voice TwiML
        
    Returns:
        tuple[bool, str | None]: (success, error_message)
    """
    try:
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url=voice_url
        )
        return bool(call and call.sid), None
    except Exception as e:
        return False, str(e)

def fetch_call_logs_api(limit=20) -> tuple[list, str | None]:
    """Fetch call logs from Twilio API.
    
    Args:
        limit (int): Maximum number of logs to fetch
        
    Returns:
        tuple[list, str | None]: (call_logs, error_message)
    """
    try:
        calls = client.calls.list(limit=limit)
        logs = [
            {
                "from": c.from_,
                "to": c.to,
                "status": c.status,
                "duration": c.duration,
                "start_time": str(c.start_time)
            } for c in calls
        ]
        return logs, None
    except Exception as e:
        return [], str(e)
