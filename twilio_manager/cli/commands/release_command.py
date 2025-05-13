from twilio_manager.core.phone_numbers import release_number, get_active_numbers
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

def display_active_numbers(numbers):
    """Display a table of active phone numbers.
    
    Args:
        numbers (list): List of phone number dictionaries
    """
    table = create_table(columns=["#", "Phone Number", "Friendly Name", "SID"])
    for idx, number in enumerate(numbers, 1):
        table.add_row(
            str(idx),
            number['phoneNumber'],
            number.get('friendlyName', 'N/A'),
            number['sid'],
            style=STYLES['data']
        )
    console.print(table)

def get_number_to_release():
    """Get the number to release from user selection.
    
    Returns:
        dict: Selected number info or None if cancelled/no numbers
    """
    # Get list of active numbers
    active_numbers = get_active_numbers()
    
    if not active_numbers:
        print_warning("No active numbers found in your account.")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return None

    print_panel("Active Numbers:", style='highlight')
    display_active_numbers(active_numbers)

    # Let user select a number by index
    max_index = len(active_numbers)
    selection = prompt_choice(
        "\nSelect a number to release (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_warning("Release cancelled.")
        return None

    return active_numbers[int(selection) - 1]

def confirm_release_action(number):
    """Confirm the release action with the user.
    
    Args:
        number (dict): Number information
        
    Returns:
        bool: True if confirmed, False if cancelled
    """
    if not confirm_action(
        f"Are you sure you want to release number {number['phoneNumber']}? "
        "This action is irreversible.",
        style='error'
    ):
        print_warning("Release cancelled.")
        return False
    return True

def execute_number_release(number):
    """Execute the release of a phone number.
    
    Args:
        number (dict): Number information to release
    """
    success = release_number(number['sid'])

    if success:
        print_success(f"Number {number['phoneNumber']} released successfully.")
    else:
        print_error(f"Failed to release number {number['phoneNumber']}.")

    prompt_choice("\nPress Enter to return", choices=[""], default="")

def handle_release_command():
    """Handle the release of a phone number."""
    from twilio_manager.cli.menus.release_menu import ReleaseMenu
    ReleaseMenu().show()
