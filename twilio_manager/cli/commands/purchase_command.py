from twilio_manager.core.phone_numbers import purchase_number, search_available_numbers

def get_country_codes():
    """Get mapping of country codes.
    
    Returns:
        dict: Mapping of country codes
    """
    return {
        "1": "+1",  # US/Canada
        "2": "+44", # UK
        "3": "+61"  # Australia
    }

def search_available_numbers_by_country(country_code):
    """Search for available numbers in a country.
    
    Args:
        country_code (str): Country code (e.g., "+1")
        
    Returns:
        list: Available numbers or None if none found
    """
    results, error = search_available_numbers(country_code)
    if error:
        return None
    return results

def purchase_phone_number(phone_number):
    """Purchase a phone number.
    
    Args:
        phone_number (str): Phone number to purchase
        
    Returns:
        Tuple[bool, Optional[str]]: (success, error_message)
    """
    return purchase_number(phone_number)

def handle_purchase_command(pre_selected_number=None):
    """Handle the purchase of a phone number.
    
    Args:
        pre_selected_number (str, optional): Phone number to purchase directly
    """
    from twilio_manager.cli.menus.purchase_menu import PurchaseMenu
    PurchaseMenu(pre_selected_number).show()
