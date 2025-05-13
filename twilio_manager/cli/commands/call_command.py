from rich.prompt import Confirm
from rich.table import Table
from twilio_manager.core.voice import make_call
from twilio_manager.core.phone_numbers import get_active_numbers
from twilio_manager.core.messaging import get_recent_contacts
from twilio_manager.shared.ui.styling import (
    console,
    clear_screen,
    print_header,
    print_panel,
    prompt_choice
)

def display_phone_numbers(numbers):
    """Display a table of available phone numbers."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", justify="right")
    table.add_column("Phone Number", style="cyan")
    table.add_column("Friendly Name", style="green")
    table.add_column("Voice Enabled", style="yellow")

    for idx, number in enumerate(numbers, 1):
        voice_enabled = "✓" if number.get('capabilities', {}).get('voice', False) else "✗"
        table.add_row(
            str(idx),
            number['phoneNumber'],
            number.get('friendlyName', 'N/A'),
            voice_enabled
        )
    
    console.print(table)

def display_recent_contacts(contacts):
    """Display a table of recent contacts."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", justify="right")
    table.add_column("Phone Number", style="cyan")
    table.add_column("Last Contact", style="green")
    table.add_column("Direction", style="yellow")

    for idx, contact in enumerate(contacts, 1):
        table.add_row(
            str(idx),
            contact['phoneNumber'],
            contact.get('lastContact', 'N/A'),
            contact.get('lastDirection', 'N/A')
        )
    
    console.print(table)

def handle_make_call_command():
    clear_screen()
    print_header("Make a Voice Call", "📞")

    # Get active numbers with voice capability
    active_numbers = [n for n in get_active_numbers() if n.get('capabilities', {}).get('voice', False)]
    
    if not active_numbers:
        print_panel("[yellow]No voice-enabled numbers found in your account.[/yellow]")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    # Select sender number
    console.print("\n[bold]Select a number to call from:[/bold]")
    display_phone_numbers(active_numbers)

    max_index = len(active_numbers)
    selection = prompt_choice(
        "\nSelect a number (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_panel("[yellow]Call cancelled.[/yellow]")
        return

    from_number = active_numbers[int(selection) - 1]['phoneNumber']

    # Get recipient number
    print_panel("\n[bold]Select recipient:[/bold]")
    recipient_choice = prompt_choice(
        "Choose an option",
        choices=["1", "2"],
        default="1"
    )
    
    if recipient_choice == "1":
        to_number = prompt_choice("Enter recipient phone number (e.g., +14155559876)", choices=None)
    else:
        recent_contacts = get_recent_contacts()
        if not recent_contacts:
            print_panel("[yellow]No recent contacts found.[/yellow]")
            to_number = prompt_choice("Enter recipient phone number (e.g., +14155559876)", choices=None)
        else:
            console.print("\n[bold]Select from recent contacts:[/bold]")
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
    print_panel("\n[bold]Select voice response:[/bold]")
    url_choice = prompt_choice(
        "Choose an option",
        choices=["1", "2"],
        default="1"
    )
    
    if url_choice == "1":
        voice_url = "https://handler.twilio.com/twiml/default-greeting"
    else:
        voice_url = prompt_choice("Enter TwiML URL", choices=None)

    # Confirm and make call
    print_panel("\n[bold]Review call details:[/bold]")
    console.print(f"From: [green]{from_number}[/green]")
    console.print(f"To: [cyan]{to_number}[/cyan]")
    console.print(f"Voice URL: [yellow]{voice_url}[/yellow]")

    confirm = Confirm.ask("\nPlace this call?")
    if not confirm:
        print_panel("[yellow]Call cancelled.[/yellow]")
        return

    success = make_call(from_number, to_number, voice_url)

    if success:
        print_panel("[green]✅ Call initiated successfully![/green]")
    else:
        print_panel("[red]❌ Failed to place the call.[/red]")

    prompt_choice("\nPress Enter to return", choices=[""], default="")
