from twilio_manager.core.messaging import send_message, get_recent_contacts
from twilio_manager.core.phone_numbers import get_active_numbers
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
    table = create_table(columns=["#", "Phone Number", "Friendly Name"])
    for idx, number in enumerate(numbers, 1):
        table.add_row(
            str(idx),
            number['phoneNumber'],
            number.get('friendlyName', 'N/A'),
            style=STYLES['data']
        )
    console.print(table)

def display_recent_contacts(contacts):
    """Display a table of recent contacts.
    
    Args:
        contacts (list): List of contact dictionaries
    """
    table = create_table(columns=["#", "Phone Number", "Last Contact"])
    for idx, contact in enumerate(contacts, 1):
        table.add_row(
            str(idx),
            contact['phoneNumber'],
            contact.get('lastContact', 'N/A'),
            style=STYLES['data']
        )
    console.print(table)

def collect_message_inputs():
    """Collect all inputs needed for sending a message.
    
    Returns:
        dict: Message inputs or None if cancelled
    """
    # Get list of active numbers
    active_numbers = get_active_numbers()
    
    if not active_numbers:
        print_warning("No active numbers found in your account.")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return None

    # Select sender number
    print_panel("Select a number to send from:", style='highlight')
    display_active_numbers(active_numbers)

    max_index = len(active_numbers)
    selection = prompt_choice(
        "\nSelect a number (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_warning("Message cancelled.")
        return None

    from_number = active_numbers[int(selection) - 1]['phoneNumber']

    # Get recent contacts
    recent_contacts = get_recent_contacts()
    
    # Select recipient
    print_panel("Select recipient:", style='highlight')
    console.print("1. Choose from recent contacts", style=STYLES['data'])
    console.print("2. Enter new number", style=STYLES['data'])
    
    recipient_choice = prompt_choice("Select option", choices=["1", "2"])
    
    if recipient_choice == "1" and recent_contacts:
        print_panel("Recent Contacts:", style='highlight')
        display_recent_contacts(recent_contacts)
        
        max_contact_index = len(recent_contacts)
        contact_selection = prompt_choice(
            "\nSelect a contact (0 to enter new number)",
            choices=[str(i) for i in range(max_contact_index + 1)]
        )
        
        if contact_selection == "0":
            to_number = prompt_choice("Enter recipient's number (E.164 format, e.g., +14155559876)", choices=None)
        else:
            to_number = recent_contacts[int(contact_selection) - 1]['phoneNumber']
    else:
        to_number = prompt_choice("Enter recipient's number (E.164 format, e.g., +14155559876)", choices=None)

    # Get message body
    body = prompt_choice("\nMessage body", choices=None)

    return {
        'from_number': from_number,
        'to_number': to_number,
        'body': body
    }

def validate_recipient_number(number):
    """Validate the recipient's phone number format.
    
    Args:
        number (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Basic E.164 format validation
    if not number.startswith('+'):
        return False
    if not number[1:].isdigit():
        return False
    if len(number) < 8 or len(number) > 15:  # E.164 length limits
        return False
    return True

def send_message_with_confirmation(from_number, to_number, body):
    """Send a message after showing summary and getting confirmation.
    
    Args:
        from_number (str): Sender's phone number
        to_number (str): Recipient's phone number
        body (str): Message body
    """
    # Show summary and confirm
    print_panel("Message Summary:", style='highlight')
    console.print("From:", style=STYLES['dim'])
    console.print(from_number, style=STYLES['info'])
    console.print("\nTo:", style=STYLES['dim'])
    console.print(to_number, style=STYLES['info'])
    console.print("\nMessage:", style=STYLES['dim'])
    console.print(body, style=STYLES['info'])

    if not confirm_action("Send this message?"):
        print_warning("Message not sent.")
        return

    success = send_message(from_number, to_number, body)

    if success:
        print_success(f"Message sent successfully to {to_number}!")
    else:
        print_error(f"Failed to send message to {to_number}.")

    prompt_choice("\nPress Enter to return", choices=[""], default="")

def get_message_sid():
    """Get message SID from user input.
    
    Returns:
        str: Message SID or None if cancelled
    """
    print_panel("Delete Message", style='highlight')
    print_info("Enter the SID of the message to delete.")
    print_info("You can find the SID in the message logs.")
    
    message_sid = prompt_choice(
        "\nMessage SID (0 to cancel)",
        choices=None,
        default="0"
    )
    
    if message_sid == "0":
        print_warning("Deletion cancelled.")
        return None
        
    return message_sid

def confirm_deletion_prompt(message_sid):
    """Confirm message deletion with the user.
    
    Args:
        message_sid (str): Message SID
        
    Returns:
        bool: True if confirmed, False if cancelled
    """
    if not confirm_action(
        f"Are you sure you want to delete message {message_sid}? "
        "This action is irreversible.",
        style='error'
    ):
        print_warning("Deletion cancelled.")
        return False
    return True

def delete_message_by_sid(message_sid):
    """Delete a message by its SID.
    
    Args:
        message_sid (str): Message SID
    """
    from twilio_manager.core.messaging import delete_message
    
    success = delete_message(message_sid)
    
    if success:
        print_success(f"Message {message_sid} deleted successfully!")
    else:
        print_error(f"Failed to delete message {message_sid}.")
    
    prompt_choice("\nPress Enter to return", choices=[""], default="")

def handle_delete_message_command():
    """Handle message deletion."""
    from twilio_manager.cli.menus.delete_message_menu import DeleteMessageMenu
    DeleteMessageMenu().show()

def handle_send_message_command():
    """Handle sending a message."""
    from twilio_manager.cli.menus.send_message_menu import SendMessageMenu
    SendMessageMenu().show()
