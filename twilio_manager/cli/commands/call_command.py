from twilio_manager.core.voice import make_call
from twilio_manager.core.phone_numbers import get_active_numbers
from twilio_manager.core.messaging import get_recent_contacts
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

def display_phone_numbers(numbers):
    """Display a table of available phone numbers."""
    table = create_table(columns=["#", "Phone Number", "Friendly Name", "Voice Enabled"])
    
    for idx, number in enumerate(numbers, 1):
        voice_enabled = "✓" if number.get('capabilities', {}).get('voice', False) else "✗"
        table.add_row(
            str(idx),
            number['phoneNumber'],
            number.get('friendlyName', 'N/A'),
            voice_enabled,
            style=STYLES['data']
        )
    
    console.print(table)

def display_recent_contacts(contacts):
    """Display a table of recent contacts."""
    table = create_table(columns=["#", "Phone Number", "Last Contact", "Direction"])
    
    for idx, contact in enumerate(contacts, 1):
        table.add_row(
            str(idx),
            contact['phoneNumber'],
            contact.get('lastContact', 'N/A'),
            contact.get('lastDirection', 'N/A'),
            style=STYLES['data']
        )
    
    console.print(table)

def handle_make_call_command():

    # Get active numbers with voice capability
    active_numbers = [n for n in get_active_numbers() if n.get('capabilities', {}).get('voice', False)]
    
    if not active_numbers:
        print_warning("No voice-enabled numbers found in your account.")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    # Select sender number
    print_panel("Select a number to call from:", style='highlight')
    display_phone_numbers(active_numbers)

    max_index = len(active_numbers)
    selection = prompt_choice(
        "\nSelect a number (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_warning("Call cancelled.")
        return

    from_number = active_numbers[int(selection) - 1]['phoneNumber']

    # Get recipient number
    print_panel("Select recipient:", style='highlight')
    recipient_choice = prompt_choice(
        "Choose an option:\n1. Enter phone number manually\n2. Select from recent contacts",
        choices=["1", "2"],
        default="1"
    )
    
    if recipient_choice == "1":
        to_number = prompt_choice("Enter recipient phone number (e.g., +14155559876)", choices=None)
    else:
        recent_contacts = get_recent_contacts()
        if not recent_contacts:
            print_warning("No recent contacts found.")
            to_number = prompt_choice("Enter recipient phone number (e.g., +14155559876)", choices=None)
        else:
            print_panel("Select from recent contacts:", style='highlight')
            display_recent_contacts(recent_contacts)
            
            contact_max = len(recent_contacts)
            contact_selection = prompt_choice(
                "\nSelect a contact (0 to enter manually)",
                choices=[str(i) for i in range(contact_max + 1)]
            )
            
            if contact_selection == "0":
                to_number = prompt_choice("Enter recipient phone number (e.g., +14155559876)", choices=None)
            else:
                to_number = recent_contacts[int(contact_selection) - 1]['phoneNumber']

    # Get voice URL with default options
    print_panel("Select voice response:", style='highlight')
    url_choice = prompt_choice(
        "Choose an option:\n1. Use default greeting\n2. Custom TwiML URL",
        choices=["1", "2"],
        default="1"
    )
    
    if url_choice == "1":
        voice_url = "https://handler.twilio.com/twiml/default-greeting"
    else:
        voice_url = prompt_choice("Enter TwiML URL", choices=None)

    # Confirm and make call
    print_panel("Review call details:", style='highlight')
    console.print("From:", style=STYLES['dim'])
    console.print(from_number, style=STYLES['success'])
    console.print("\nTo:", style=STYLES['dim'])
    console.print(to_number, style=STYLES['info'])
    console.print("\nVoice URL:", style=STYLES['dim'])
    console.print(voice_url, style=STYLES['warning'])

    if not confirm_action("\nPlace this call?"):
        print_warning("Call cancelled.")
        return

    success = make_call(from_number, to_number, voice_url)

    if success:
        print_success("Call initiated successfully!")
    else:
        print_error("Failed to place the call.")

    prompt_choice("\nPress Enter to return", choices=[""], default="")
