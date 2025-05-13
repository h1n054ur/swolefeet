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

def handle_configure_command():

    # Get active numbers
    active_numbers = get_active_numbers()
    
    if not active_numbers:
        print_warning("No active numbers found in your account.")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

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
        return

    selected_number = active_numbers[int(selection) - 1]
    
    # Show current settings
    print_panel("Current Settings", style='highlight')
    print_info(f"Phone Number: {selected_number['phoneNumber']}")
    console.print("Friendly Name:", style=STYLES['dim'])
    console.print(selected_number.get('friendlyName', 'N/A'), style=STYLES['info'])
    console.print("\nVoice URL:", style=STYLES['dim'])
    console.print(selected_number.get('voiceUrl', 'N/A'), style=STYLES['info'])
    console.print("\nSMS URL:", style=STYLES['dim'])
    console.print(selected_number.get('smsUrl', 'N/A'), style=STYLES['info'])

    # Configuration options
    print_panel("What would you like to configure?", style='highlight')
    console.print("1. Friendly Name", style=STYLES['data'])
    console.print("2. Voice Webhook URL", style=STYLES['data'])
    console.print("3. SMS Webhook URL", style=STYLES['data'])
    console.print("4. All Settings", style=STYLES['data'])
    
    config_choice = prompt_choice("Select option", choices=["1", "2", "3", "4"])
    
    friendly_name = None
    voice_url = None
    sms_url = None
    
    if config_choice in ["1", "4"]:
        friendly_name = prompt_choice(
            "Enter new friendly name",
            choices=None,
            default=selected_number.get('friendlyName', '')
        )
    
    if config_choice in ["2", "4"]:
        voice_url = prompt_choice(
            "Enter new voice webhook URL",
            choices=None,
            default=selected_number.get('voiceUrl', '')
        )
    
    if config_choice in ["3", "4"]:
        sms_url = prompt_choice(
            "Enter new SMS webhook URL",
            choices=None,
            default=selected_number.get('smsUrl', '')
        )

    # Show summary of changes
    print_panel("Review Changes", style='highlight')
    if friendly_name:
        console.print("Friendly Name:", style=STYLES['dim'])
        console.print(selected_number.get('friendlyName', 'N/A'), style=STYLES['error'])
        console.print("→", style=STYLES['dim'])
        console.print(friendly_name, style=STYLES['success'])
    if voice_url:
        console.print("\nVoice URL:", style=STYLES['dim'])
        console.print(selected_number.get('voiceUrl', 'N/A'), style=STYLES['error'])
        console.print("→", style=STYLES['dim'])
        console.print(voice_url, style=STYLES['success'])
    if sms_url:
        console.print("\nSMS URL:", style=STYLES['dim'])
        console.print(selected_number.get('smsUrl', 'N/A'), style=STYLES['error'])
        console.print("→", style=STYLES['dim'])
        console.print(sms_url, style=STYLES['success'])

    if not confirm_action("\nApply these changes?"):
        print_warning("Configuration cancelled.")
        return

    success = configure_number(
        selected_number['sid'],
        friendly_name=friendly_name,
        voice_url=voice_url,
        sms_url=sms_url
    )

    if success:
        print_success("Number configured successfully!")
    else:
        print_error("Failed to update number settings.")

    prompt_choice("\nPress Enter to return", choices=[""], default="")
