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

def handle_purchase_command(pre_selected_number=None):
    """Handle the purchase of a phone number.
    
    Args:
        pre_selected_number (str, optional): Phone number to purchase directly
    """


    if pre_selected_number:
        # If number is pre-selected (e.g., from search), confirm and purchase
        if not confirm_action(f"Are you sure you want to purchase {pre_selected_number}?"):
            print_warning("Purchase cancelled.")
            return

        success = purchase_number(pre_selected_number)

        if success:
            print_success(f"Number {pre_selected_number} purchased successfully!")
        else:
            print_error(f"Failed to purchase number {pre_selected_number}.")

        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    # If no pre-selected number, show search interface
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

    # Search for available numbers
    available_numbers = search_available_numbers(country_code)
    
    if not available_numbers:
        print_error("No numbers available in the selected region.")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    print_panel("Available Numbers:", style='highlight')
    display_number_options(available_numbers)

    # Let user select a number by index
    max_index = len(available_numbers)
    selection = prompt_choice(
        "\nSelect a number to purchase (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_warning("Purchase cancelled.")
        return

    selected_number = available_numbers[int(selection) - 1]['phoneNumber']
    if not confirm_action(f"Are you sure you want to purchase {selected_number}?"):
        print_warning("Purchase cancelled.")
        return

    success = purchase_number(selected_number)

    if success:
        print_success(f"Number {selected_number} purchased successfully!")
    else:
        print_error(f"Failed to purchase number {selected_number}.")

    prompt_choice("\nPress Enter to return", choices=[""], default="")
