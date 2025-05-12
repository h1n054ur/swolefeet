from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from twilio_manager.core.messaging import send_message, get_recent_contacts
from twilio_manager.core.phone_numbers import get_active_numbers

console = Console()

def display_active_numbers(numbers):
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
    console.clear()
    console.print(Panel.fit("[bold cyan]✉️ Send a Message[/bold cyan]"))

    # Get list of active numbers
    active_numbers = get_active_numbers()
    
    if not active_numbers:
        console.print("[yellow]No active numbers found in your account.[/yellow]")
        Prompt.ask("\nPress Enter to return")
        return

    # Select sender number
    console.print("\n[bold]Select a number to send from:[/bold]")
    display_active_numbers(active_numbers)

    max_index = len(active_numbers)
    selection = Prompt.ask(
        "\nSelect a number (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        console.print("[yellow]Message cancelled.[/yellow]")
        return

    from_number = active_numbers[int(selection) - 1]['phoneNumber']

    # Get recent contacts
    recent_contacts = get_recent_contacts()
    
    # Select recipient
    console.print("\n[bold]Select recipient:[/bold]")
    console.print("1. Choose from recent contacts")
    console.print("2. Enter new number")
    
    recipient_choice = Prompt.ask("Select option", choices=["1", "2"])
    
    if recipient_choice == "1" and recent_contacts:
        console.print("\n[bold]Recent Contacts:[/bold]")
        display_recent_contacts(recent_contacts)
        
        max_contact_index = len(recent_contacts)
        contact_selection = Prompt.ask(
            "\nSelect a contact (0 to enter new number)",
            choices=[str(i) for i in range(max_contact_index + 1)]
        )
        
        if contact_selection == "0":
            to_number = Prompt.ask("Enter recipient's number (E.164 format, e.g., +14155559876)")
        else:
            to_number = recent_contacts[int(contact_selection) - 1]['phoneNumber']
    else:
        to_number = Prompt.ask("Enter recipient's number (E.164 format, e.g., +14155559876)")

    # Get message body
    body = Prompt.ask("\nMessage body")

    # Show summary and confirm
    console.print("\n[bold]Message Summary:[/bold]")
    console.print(f"From: [cyan]{from_number}[/cyan]")
    console.print(f"To: [cyan]{to_number}[/cyan]")
    console.print(f"Message:\n[green]{body}[/green]\n")

    confirm = Confirm.ask("Send this message?")
    if not confirm:
        console.print("[yellow]Message not sent.[/yellow]")
        return

    success = send_message(from_number, to_number, body)

    if success:
        console.print(f"[green]✅ Message sent successfully to {to_number}![/green]")
    else:
        console.print(f"[red]❌ Failed to send message to {to_number}.[/red]")

    Prompt.ask("\nPress Enter to return")
