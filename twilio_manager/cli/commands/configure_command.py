from twilio_manager.core.phone_numbers import configure_number, get_active_numbers

def get_active_numbers_list():
    """Get list of active phone numbers.
    
    Returns:
        list: List of active phone numbers or None if none found
    """
    return get_active_numbers()

def configure_phone_number(number_sid, friendly_name=None, voice_url=None, sms_url=None):
    """Configure a phone number's settings.
    
    Args:
        number_sid (str): SID of the number to configure
        friendly_name (str, optional): New friendly name
        voice_url (str, optional): New voice webhook URL
        sms_url (str, optional): New SMS webhook URL
        
    Returns:
        bool: True if configuration successful, False otherwise
    """
    return configure_number(
        number_sid,
        friendly_name=friendly_name,
        voice_url=voice_url,
        sms_url=sms_url
    )

def handle_configure_command():
    """Handle the configuration of a phone number."""
    from twilio_manager.cli.menus.configure_menu import ConfigureMenu
    ConfigureMenu().show()
