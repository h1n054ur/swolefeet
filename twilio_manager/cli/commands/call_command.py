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

def collect_call_inputs():
    """Collect all inputs needed for making a voice call.
    
    Returns:
        dict: Call inputs or None if cancelled
    """
    # Get active numbers with voice capability
    active_numbers = [n for n in get_active_numbers() if n.get('capabilities', {}).get('voice', False)]
    
    if not active_numbers:
        print_warning("No voice-enabled numbers found in your account.")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return None

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
        return None

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

    return {
        'from_number': from_number,
        'to_number': to_number,
        'voice_url': voice_url
    }

def initiate_call(from_number, to_number, voice_url):
    """Initiate a voice call with confirmation.
    
    Args:
        from_number (str): Caller's phone number
        to_number (str): Recipient's phone number
        voice_url (str): TwiML URL for call handling
    """
    # Show call details and confirm
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

def get_recordings():
    """Get list of call recordings.
    
    Returns:
        list: List of recording dictionaries
    """
    from twilio_manager.core.voice import get_recordings as fetch_recordings
    return fetch_recordings()

def display_recordings(recordings):
    """Display recordings in a table.
    
    Args:
        recordings (list): List of recording dictionaries
    """
    table = create_table(
        columns=["#", "SID", "Call SID", "Duration", "Date"],
        title="Call Recordings"
    )

    for idx, recording in enumerate(recordings, 1):
        table.add_row(
            str(idx),
            recording.get('sid', '—'),
            recording.get('call_sid', '—'),
            str(recording.get('duration', '0')) + "s",
            recording.get('date_created', '—'),
            style=STYLES['data']
        )

    console.print(table)

def get_recording_sid():
    """Get recording SID from user input.
    
    Returns:
        str: Recording SID or None if cancelled
    """
    recording_sid = prompt_choice(
        "\nEnter recording SID to delete (0 to cancel)",
        choices=None,
        default="0"
    )

    if recording_sid == "0":
        print_warning("Deletion cancelled.")
        return None

    return recording_sid

def delete_recording(recording_sid):
    """Delete a recording by its SID.
    
    Args:
        recording_sid (str): Recording SID
    """
    from twilio_manager.core.voice import delete_recording as remove_recording

    if not confirm_action(
        f"Are you sure you want to delete recording {recording_sid}? "
        "This action cannot be undone.",
        style='error'
    ):
        print_warning("Deletion cancelled.")
        return

    success = remove_recording(recording_sid)

    if success:
        print_success(f"Recording {recording_sid} deleted successfully!")
    else:
        print_error(f"Failed to delete recording {recording_sid}.")

    prompt_choice("\nPress Enter to return", choices=[""], default="")

def handle_manage_recordings():
    """Handle recording management."""
    from twilio_manager.cli.menus.recordings_menu import RecordingsMenu
    RecordingsMenu().show()

def list_conferences():
    """Get list of active conferences.
    
    Returns:
        list: List of conference dictionaries
    """
    from twilio_manager.core.voice import get_conferences
    return get_conferences()

def display_conferences(conferences):
    """Display conferences in a table.
    
    Args:
        conferences (list): List of conference dictionaries
    """
    table = create_table(
        columns=["#", "SID", "Name", "Status", "Participants"],
        title="Active Conferences"
    )

    for idx, conf in enumerate(conferences, 1):
        table.add_row(
            str(idx),
            conf.get('sid', '—'),
            conf.get('friendly_name', '—'),
            conf.get('status', '—'),
            str(conf.get('participant_count', 0)),
            style=STYLES['data']
        )

    console.print(table)

def get_conference_sid(action):
    """Get conference SID from user input.
    
    Args:
        action (str): Action being performed ('join' or 'end')
        
    Returns:
        str: Conference SID or None if cancelled
    """
    conference_sid = prompt_choice(
        f"\nEnter conference SID to {action} (0 to cancel)",
        choices=None,
        default="0"
    )

    if conference_sid == "0":
        print_warning(f"Conference {action} cancelled.")
        return None

    return conference_sid

def join_conference(conference_sid):
    """Join a conference call.
    
    Args:
        conference_sid (str): Conference SID
    """
    from twilio_manager.core.voice import join_conference as join_conf
    
    # Get active numbers with voice capability
    active_numbers = [n for n in get_active_numbers() if n.get('capabilities', {}).get('voice', False)]
    
    if not active_numbers:
        print_warning("No voice-enabled numbers found in your account.")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    # Select number to join with
    print_panel("Select a number to join with:", style='highlight')
    display_phone_numbers(active_numbers)

    max_index = len(active_numbers)
    selection = prompt_choice(
        "\nSelect a number (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_warning("Conference join cancelled.")
        return

    from_number = active_numbers[int(selection) - 1]['phoneNumber']

    success = join_conf(conference_sid, from_number)

    if success:
        print_success(f"Successfully joined conference {conference_sid}!")
    else:
        print_error(f"Failed to join conference {conference_sid}.")

    prompt_choice("\nPress Enter to return", choices=[""], default="")

def end_conference(conference_sid):
    """End a conference call.
    
    Args:
        conference_sid (str): Conference SID
    """
    from twilio_manager.core.voice import end_conference as end_conf

    if not confirm_action(
        f"Are you sure you want to end conference {conference_sid}? "
        "All participants will be disconnected.",
        style='error'
    ):
        print_warning("Conference end cancelled.")
        return

    success = end_conf(conference_sid)

    if success:
        print_success(f"Conference {conference_sid} ended successfully!")
    else:
        print_error(f"Failed to end conference {conference_sid}.")

    prompt_choice("\nPress Enter to return", choices=[""], default="")

def handle_conference_calls():
    """Handle conference call management."""
    from twilio_manager.cli.menus.conference_menu import ConferenceMenu
    ConferenceMenu().show()

def handle_make_call_command():
    """Handle making a voice call."""
    from twilio_manager.cli.menus.call_menu import CallMenu
    CallMenu().show()
