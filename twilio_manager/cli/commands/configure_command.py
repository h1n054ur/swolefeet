from rich.prompt import Confirm
from rich.table import Table
from twilio_manager.core.phone_numbers import configure_number, get_active_numbers
from twilio_manager.shared.ui.styling import (
    console,
    clear_screen,
    print_header,
    print_panel,
    prompt_choice
)

def display_active_numbers(numbers):
    """Display a table of active phone numbers."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", justify="right")
    table.add_column("Phone Number", style="cyan")
    table.add_column("Friendly Name", style="green")
    table.add_column("Voice URL", style="yellow")
    table.add_column("SMS URL", style="yellow")

    for idx, number in enumerate(numbers, 1):
        table.add_row(
            str(idx),
            number['phoneNumber'],
            number.get('friendlyName', 'N/A'),
            number.get('voiceUrl', 'N/A'),
            number.get('smsUrl', 'N/A')
        )
    
    console.print(table)

def handle_configure_command():
    clear_screen()
    print_header("Configure a Phone Number", "⚙️")

    # Get active numbers
    active_numbers = get_active_numbers()
    
    if not active_numbers:
        print_panel("[yellow]No active numbers found in your account.[/yellow]")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    # Display active numbers
    print_panel("\n[bold]Select a number to configure:[/bold]")
    display_active_numbers(active_numbers)

    # Select number
    max_index = len(active_numbers)
    selection = prompt_choice(
        "\nSelect a number (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_panel("[yellow]Configuration cancelled.[/yellow]")
        return

    selected_number = active_numbers[int(selection) - 1]
    
    # Show current settings
    print_panel(
        f"Current settings for {selected_number['phoneNumber']}:\n"
        f"Friendly Name: [cyan]{selected_number.get('friendlyName', 'N/A')}[/cyan]\n"
        f"Voice URL: [cyan]{selected_number.get('voiceUrl', 'N/A')}[/cyan]\n"
        f"SMS URL: [cyan]{selected_number.get('smsUrl', 'N/A')}[/cyan]"
    )

    # Configuration options
    print_panel(
        "[bold]What would you like to configure?[/bold]\n"
        "1. Friendly Name\n"
        "2. Voice Webhook URL\n"
        "3. SMS Webhook URL\n"
        "4. All Settings"
    )
    
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
    changes_summary = "[bold]Review Changes:[/bold]\n"
    if friendly_name:
        changes_summary += f"Friendly Name: [red]{selected_number.get('friendlyName', 'N/A')}[/red] → [green]{friendly_name}[/green]\n"
    if voice_url:
        changes_summary += f"Voice URL: [red]{selected_number.get('voiceUrl', 'N/A')}[/red] → [green]{voice_url}[/green]\n"
    if sms_url:
        changes_summary += f"SMS URL: [red]{selected_number.get('smsUrl', 'N/A')}[/red] → [green]{sms_url}[/green]"
    
    print_panel(changes_summary)

    confirm = Confirm.ask("\n[bold yellow]Apply these changes?[/bold yellow]")
    if not confirm:
        print_panel("[yellow]Configuration cancelled.[/yellow]")
        return

    success = configure_number(
        selected_number['sid'],
        friendly_name=friendly_name,
        voice_url=voice_url,
        sms_url=sms_url
    )

    if success:
        print_panel("[green]✅ Number configured successfully![/green]")
    else:
        print_panel("[red]❌ Failed to update number settings.[/red]")

    prompt_choice("\nPress Enter to return", choices=[""], default="")
