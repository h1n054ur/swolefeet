from twilio_manager.core.phone_numbers import configure_number, get_active_numbers
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
    """Display a table of active phone numbers."""
    table = create_table(columns=["#", "Phone Number", "Friendly Name", "Voice URL", "SMS URL"])

    for idx, number in enumerate(numbers, 1):
        table.add_row(
            str(idx),
            number['phoneNumber'],
            number.get('friendlyName', 'N/A'),
            number.get('voiceUrl', 'N/A'),
            number.get('smsUrl', 'N/A'),
            style=STYLES['data']
        )
    
    console.print(table)

def get_number_selection():
    """Get user's number selection from active numbers.
    
    Returns:
        dict: Selected number info or None if cancelled/no numbers
    """
    # Get active numbers
    active_numbers = get_active_numbers()
    
    if not active_numbers:
        print_warning("No active numbers found in your account.")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return None

    # Display active numbers
    print_panel("Select a number to configure:", style='highlight')
    display_active_numbers(active_numbers)

    # Select number
    max_index = len(active_numbers)
    selection = prompt_choice(
        "\nSelect a number (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_warning("Configuration cancelled.")
        return None

    return active_numbers[int(selection) - 1]

def show_current_settings(number):
    """Display current settings for a number.
    
    Args:
        number (dict): Number information
    """
    print_panel("Current Settings", style='highlight')
    print_info(f"Phone Number: {number['phoneNumber']}")
    console.print("Friendly Name:", style=STYLES['dim'])
    console.print(number.get('friendlyName', 'N/A'), style=STYLES['info'])
    console.print("\nVoice URL:", style=STYLES['dim'])
    console.print(number.get('voiceUrl', 'N/A'), style=STYLES['info'])
    console.print("\nSMS URL:", style=STYLES['dim'])
    console.print(number.get('smsUrl', 'N/A'), style=STYLES['info'])

def collect_configuration_changes(number):
    """Collect configuration changes from user.
    
    Args:
        number (dict): Current number settings
        
    Returns:
        dict: Configuration changes or None if cancelled
    """
    # Configuration options
    print_panel("What would you like to configure?", style='highlight')
    console.print("1. Friendly Name", style=STYLES['data'])
    console.print("2. Voice Webhook URL", style=STYLES['data'])
    console.print("3. SMS Webhook URL", style=STYLES['data'])
    console.print("4. All Settings", style=STYLES['data'])
    
    config_choice = prompt_choice("Select option", choices=["1", "2", "3", "4"])
    
    changes = {}
    
    if config_choice in ["1", "4"]:
        changes['friendly_name'] = prompt_choice(
            "Enter new friendly name",
            choices=None,
            default=number.get('friendlyName', '')
        )
    
    if config_choice in ["2", "4"]:
        changes['voice_url'] = prompt_choice(
            "Enter new voice webhook URL",
            choices=None,
            default=number.get('voiceUrl', '')
        )
    
    if config_choice in ["3", "4"]:
        changes['sms_url'] = prompt_choice(
            "Enter new SMS webhook URL",
            choices=None,
            default=number.get('smsUrl', '')
        )

    # Show summary of changes
    print_panel("Review Changes", style='highlight')
    if changes.get('friendly_name'):
        console.print("Friendly Name:", style=STYLES['dim'])
        console.print(number.get('friendlyName', 'N/A'), style=STYLES['error'])
        console.print("→", style=STYLES['dim'])
        console.print(changes['friendly_name'], style=STYLES['success'])
    if changes.get('voice_url'):
        console.print("\nVoice URL:", style=STYLES['dim'])
        console.print(number.get('voiceUrl', 'N/A'), style=STYLES['error'])
        console.print("→", style=STYLES['dim'])
        console.print(changes['voice_url'], style=STYLES['success'])
    if changes.get('sms_url'):
        console.print("\nSMS URL:", style=STYLES['dim'])
        console.print(number.get('smsUrl', 'N/A'), style=STYLES['error'])
        console.print("→", style=STYLES['dim'])
        console.print(changes['sms_url'], style=STYLES['success'])

    if not confirm_action("\nApply these changes?"):
        print_warning("Configuration cancelled.")
        return None

    return changes

def apply_configuration_changes(number_sid, changes):
    """Apply configuration changes to a number.
    
    Args:
        number_sid (str): SID of the number to configure
        changes (dict): Configuration changes to apply
    """
    success = configure_number(
        number_sid,
        friendly_name=changes.get('friendly_name'),
        voice_url=changes.get('voice_url'),
        sms_url=changes.get('sms_url')
    )

    if success:
        print_success("Number configured successfully!")
    else:
        print_error("Failed to update number settings.")

    prompt_choice("\nPress Enter to return", choices=[""], default="")

def handle_configure_command():
    """Handle the configuration of a phone number."""
    from twilio_manager.cli.menus.configure_menu import ConfigureMenu
    ConfigureMenu().show()
