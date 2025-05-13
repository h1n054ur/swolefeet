from twilio_manager.core.phone_numbers import purchase_number, search_available_numbers
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_panel,
    print_success,
    print_error,
    print_warning,
    print_info,
    prompt_choice,
    confirm_action,
    STYLES
)

def display_number_options(numbers):
    """Display a table of available phone numbers.
    
    Args:
        numbers (list): List of phone number dictionaries
    """
    table = create_table(columns=["#", "Phone Number", "Region", "Monthly Cost"])
    for idx, number in enumerate(numbers, 1):
        table.add_row(
            str(idx),
            number['phoneNumber'],
            f"{number.get('region', 'N/A')}",
            f"${number.get('monthlyPrice', 'N/A')}",
            style=STYLES['data']
        )
    console.print(table)

def collect_purchase_parameters():
    """Collect parameters for purchasing a number.
    
    Returns:
        dict: Search parameters or None if cancelled
    """
    print_panel("Search for available numbers:", style='highlight')
    console.print("1. US/Canada (+1)", style=STYLES['data'])
    console.print("2. UK (+44)", style=STYLES['data'])
    console.print("3. Australia (+61)", style=STYLES['data'])
    console.print("4. Other (specify country code)", style=STYLES['data'])

    country_choice = prompt_choice("Select country", choices=["1", "2", "3", "4"], default="1")
    country_codes = {
        "1": "+1",
        "2": "+44",
        "3": "+61"
    }
    
    country_code = country_codes.get(country_choice)
    if country_choice == "4":
        country_code = prompt_choice("Enter country code (with +)", choices=None)

    return {'country_code': country_code}

def search_and_display_numbers(params):
    """Search for available numbers and display them.
    
    Args:
        params (dict): Search parameters
        
    Returns:
        list: Available numbers or None if none found
    """
    available_numbers = search_available_numbers(params['country_code'])
    
    if not available_numbers:
        print_error("No numbers available in the selected region.")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return None

    print_panel("Available Numbers:", style='highlight')
    display_number_options(available_numbers)
    return available_numbers

def confirm_purchase_choice(phone_number):
    """Confirm purchase with the user.
    
    Args:
        phone_number (str): Phone number to purchase
        
    Returns:
        bool: True if confirmed, False if cancelled
    """
    if not confirm_action(f"Are you sure you want to purchase {phone_number}?"):
        print_warning("Purchase cancelled.")
        return False
    return True

def execute_number_purchase(phone_number):
    """Execute the purchase of a phone number.
    
    Args:
        phone_number (str): Phone number to purchase
    """
    success = purchase_number(phone_number)

    if success:
        print_success(f"Number {phone_number} purchased successfully!")
    else:
        print_error(f"Failed to purchase number {phone_number}.")

    prompt_choice("\nPress Enter to return", choices=[""], default="")

def handle_purchase_command(pre_selected_number=None):
    """Handle the purchase of a phone number.
    
    Args:
        pre_selected_number (str, optional): Phone number to purchase directly
    """
    from twilio_manager.cli.menus.purchase_menu import PurchaseMenu
    PurchaseMenu(pre_selected_number).show()
