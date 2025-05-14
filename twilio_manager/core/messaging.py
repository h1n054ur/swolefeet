from twilio_manager.services.messaging_service import (
    send_message_api,
    fetch_message_logs_api,
    get_recent_contacts_api
)

def send_message(from_number, to_number, body) -> tuple[bool, str | None]:
    """Send a message.
    
    Args:
        from_number (str): Sender phone number
        to_number (str): Recipient phone number
        body (str): Message content
        
    Returns:
        tuple[bool, str | None]: (success, error_message)
    """
    try:
        success = send_message_api(from_number, to_number, body)
        return success, None
    except Exception as e:
        return False, str(e)

def get_message_logs() -> tuple[list, str | None]:
    """Get message logs.
    
    Returns:
        tuple[list, str | None]: (message_logs, error_message)
    """
    try:
        logs = fetch_message_logs_api()
        return logs, None
    except Exception as e:
        return [], str(e)

def get_recent_contacts(limit=10) -> tuple[list, str | None]:
    """Get a list of unique recent contacts.
    
    Args:
        limit (int): Maximum number of contacts to return
        
    Returns:
        tuple[list, str | None]: (contacts_list, error_message)
    """
    try:
        contacts = get_recent_contacts_api(limit)
        return contacts, None
    except Exception as e:
        return [], str(e)
