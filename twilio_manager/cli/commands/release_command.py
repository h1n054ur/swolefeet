from twilio_manager.core.phone_numbers import release_number, get_active_numbers

def get_active_numbers_list():
    """Get list of active phone numbers.
    
    Returns:
        list: List of active phone numbers or None if none found
    """
    return get_active_numbers()

def release_phone_number(number_sid):
    """Release a phone number.
    
    Args:
        number_sid (str): SID of the number to release
        
    Returns:
        bool: True if release successful, False otherwise
    """
    return release_number(number_sid)

def handle_release_command():
    """Handle the release of a phone number."""
    from twilio_manager.cli.menus.release_menu import ReleaseMenu
    ReleaseMenu().show()
