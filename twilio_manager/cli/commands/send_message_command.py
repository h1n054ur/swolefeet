from twilio_manager.core.messaging import send_message, get_recent_contacts
from twilio_manager.core.phone_numbers import get_active_numbers

def get_active_numbers_list():
    """Get list of active numbers.
    
    Returns:
        list: List of active phone numbers or None if none found
    """
    return get_active_numbers()

def get_recent_contacts_list():
    """Get list of recent contacts.
    
    Returns:
        list: List of recent contacts
    """
    return get_recent_contacts()

def prepare_message_params(from_number, to_number, body):
    """Prepare message parameters.
    
    Args:
        from_number (str): Sender's phone number
        to_number (str): Recipient's phone number
        body (str): Message body
        
    Returns:
        dict: Message parameters
    """
    return {
        'from_number': from_number,
        'to_number': to_number,
        'body': body
    }

def validate_recipient_number(number):
    """Validate the recipient's phone number format.
    
    Args:
        number (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Basic E.164 format validation
    if not number.startswith('+'):
        return False
    if not number[1:].isdigit():
        return False
    if len(number) < 8 or len(number) > 15:  # E.164 length limits
        return False
    return True

def send_sms_message(params):
    """Send a message using the provided parameters.
    
    Args:
        params (dict): Message parameters with from_number, to_number, and body
        
    Returns:
        bool: True if message sent successfully, False otherwise
    """
    return send_message(params['from_number'], params['to_number'], params['body'])

def delete_message_by_sid(message_sid):
    """Delete a message by its SID.
    
    Args:
        message_sid (str): Message SID
        
    Returns:
        bool: True if message deleted successfully, False otherwise
    """
    from twilio_manager.core.messaging import delete_message
    return delete_message(message_sid)

def handle_delete_message_command():
    """Handle message deletion."""
    from twilio_manager.cli.menus.delete_message_menu import DeleteMessageMenu
    DeleteMessageMenu().show()

def handle_send_message_command():
    """Handle sending a message."""
    from twilio_manager.cli.menus.send_message_menu import SendMessageMenu
    SendMessageMenu().show()
