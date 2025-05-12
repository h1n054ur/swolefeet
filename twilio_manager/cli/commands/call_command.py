from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from twilio_manager.core.voice import make_call
from twilio_manager.core.phone_numbers import get_active_numbers
from twilio_manager.core.messaging import get_recent_contacts

console = Console()

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
    console.clear()
    console.print(Panel.fit("[bold cyan]📞 Make a Voice Call[/bold cyan]"))

    # Get active numbers with voice capability
    active_numbers = [n for n in get_active_numbers() if n.get('capabilities', {}).get('voice', False)]
    
    if not active_numbers:
        console.print("[yellow]No voice-enabled numbers found in your account.[/yellow]")
        Prompt.ask("\nPress Enter to return")
        return

    # Select sender number
    console.print("\n[bold]Select a number to call from:[/bold]")
    display_phone_numbers(active_numbers)

    max_index = len(active_numbers)
    selection = Prompt.ask(
        "\nSelect a number (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        console.print("[yellow]Call cancelled.[/yellow]")
        return

    from_number = active_numbers[int(selection) - 1]['phoneNumber']

    # Get recipient number
    console.print("\n[bold]Select recipient:[/bold]")
    console.print("1. Enter phone number manually")
    console.print("2. Select from recent contacts")
    
    recipient_choice = Prompt.ask("Choose an option", choices=["1", "2"])
    
    if recipient_choice == "1":
        to_number = Prompt.ask("Enter recipient phone number (e.g., +14155559876)")
    else:
        recent_contacts = get_recent_contacts()
        if not recent_contacts:
            console.print("[yellow]No recent contacts found.[/yellow]")
            to_number = Prompt.ask("Enter recipient phone number (e.g., +14155559876)")
        else:
            console.print("\n[bold]Select from recent contacts:[/bold]")
            display_recent_contacts(recent_contacts)
            
            contact_max = len(recent_contacts)
            contact_selection = Prompt.ask(
                "\nSelect a contact (0 to enter manually)",
                choices=[str(i) for i in range(contact_max + 1)]
            )
            
            if contact_selection == "0":
                to_number = Prompt.ask("Enter recipient phone number (e.g., +14155559876)")
            else:
                to_number = recent_contacts[int(contact_selection) - 1]['phoneNumber']

    # Get voice URL with default options
    console.print("\n[bold]Select voice response:[/bold]")
    console.print("1. Default greeting")
    console.print("2. Custom TwiML URL")
    
    url_choice = Prompt.ask("Choose an option", choices=["1", "2"])
    
    if url_choice == "1":
        voice_url = "https://handler.twilio.com/twiml/default-greeting"
    else:
        voice_url = Prompt.ask("Enter TwiML URL")

    # Confirm and make call
    console.print("\n[bold]Review call details:[/bold]")
    console.print(f"From: [green]{from_number}[/green]")
    console.print(f"To: [cyan]{to_number}[/cyan]")
    console.print(f"Voice URL: [yellow]{voice_url}[/yellow]")

    confirm = Confirm.ask("\nPlace this call?")
    if not confirm:
        console.print("[yellow]Call cancelled.[/yellow]")
        return

    success = make_call(from_number, to_number, voice_url)

    if success:
        console.print(f"[green]✅ Call initiated successfully![/green]")
    else:
        console.print(f"[red]❌ Failed to place the call.[/red]")

    Prompt.ask("\nPress Enter to return")
