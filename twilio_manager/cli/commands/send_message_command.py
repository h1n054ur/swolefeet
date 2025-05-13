from rich.prompt import Confirm
from rich.table import Table
from twilio_manager.core.messaging import send_message, get_recent_contacts
from twilio_manager.core.phone_numbers import get_active_numbers
from twilio_manager.shared.ui.styling import (
    console,
    clear_screen,
    print_header,
    print_panel,
    prompt_choice
)

def display_active_numbers(numbers):
    """Display a table of active phone numbers.
    
    Args:
        numbers (list): List of phone number dictionaries
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim")
    table.add_column("Phone Number", style="cyan")
    table.add_column("Friendly Name", style="green")

    for idx, number in enumerate(numbers, 1):
        table.add_row(
            str(idx),
            number['phoneNumber'],
            number.get('friendlyName', 'N/A')
        )
    
    console.print(table)

def display_recent_contacts(contacts):
    """Display a table of recent contacts.
    
    Args:
        contacts (list): List of contact dictionaries
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim")
    table.add_column("Phone Number", style="cyan")
    table.add_column("Last Contact", style="green")

    for idx, contact in enumerate(contacts, 1):
        table.add_row(
            str(idx),
            contact['phoneNumber'],
            contact.get('lastContact', 'N/A')
        )
    
    console.print(table)

def handle_send_message_command():
    """Handle sending a message."""
    clear_screen()
    print_header("Send a Message", "✉️")

    # Get list of active numbers
    active_numbers = get_active_numbers()
    
    if not active_numbers:
        print_panel("[yellow]No active numbers found in your account.[/yellow]")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    # Select sender number
    print_panel("[bold]Select a number to send from:[/bold]")
    display_active_numbers(active_numbers)

    max_index = len(active_numbers)
    selection = prompt_choice(
        "\nSelect a number (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_panel("[yellow]Message cancelled.[/yellow]")
        return

    from_number = active_numbers[int(selection) - 1]['phoneNumber']

    # Get recent contacts
    recent_contacts = get_recent_contacts()
    
    # Select recipient
    print_panel(
        "[bold]Select recipient:[/bold]\n"
        "1. Choose from recent contacts\n"
        "2. Enter new number"
    )
    
    recipient_choice = prompt_choice("Select option", choices=["1", "2"])
    
    if recipient_choice == "1" and recent_contacts:
        print_panel("[bold]Recent Contacts:[/bold]")
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

    # Show summary and confirm
    summary = (
        "[bold]Message Summary:[/bold]\n"
        f"From: [cyan]{from_number}[/cyan]\n"
        f"To: [cyan]{to_number}[/cyan]\n"
        f"Message:\n[green]{body}[/green]"
    )
    print_panel(summary)

    confirm = Confirm.ask("Send this message?")
    if not confirm:
        print_panel("[yellow]Message not sent.[/yellow]")
        return

    success = send_message(from_number, to_number, body)

    if success:
        print_panel(f"[green]✅ Message sent successfully to {to_number}![/green]")
    else:
        print_panel(f"[red]❌ Failed to send message to {to_number}.[/red]")

    prompt_choice("\nPress Enter to return", choices=[""], default="")
