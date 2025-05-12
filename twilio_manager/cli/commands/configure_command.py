from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from twilio_manager.core.phone_numbers import configure_number, get_active_numbers

console = Console()

def display_active_numbers(numbers):
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
    console.clear()
    console.print(Panel.fit("[bold cyan]⚙️ Configure a Phone Number[/bold cyan]"))

    # Get active numbers
    active_numbers = get_active_numbers()
    
    if not active_numbers:
        console.print("[yellow]No active numbers found in your account.[/yellow]")
        Prompt.ask("\nPress Enter to return")
        return

    # Display active numbers
    console.print("\n[bold]Select a number to configure:[/bold]")
    display_active_numbers(active_numbers)

    # Select number
    max_index = len(active_numbers)
    selection = Prompt.ask(
        "\nSelect a number (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        console.print("[yellow]Configuration cancelled.[/yellow]")
        return

    selected_number = active_numbers[int(selection) - 1]
    
    # Show current settings
    console.print(f"\n[bold]Current settings for {selected_number['phoneNumber']}:[/bold]")
    console.print(f"Friendly Name: [cyan]{selected_number.get('friendlyName', 'N/A')}[/cyan]")
    console.print(f"Voice URL: [cyan]{selected_number.get('voiceUrl', 'N/A')}[/cyan]")
    console.print(f"SMS URL: [cyan]{selected_number.get('smsUrl', 'N/A')}[/cyan]")

    # Configuration options
    console.print("\n[bold]What would you like to configure?[/bold]")
    console.print("1. Friendly Name")
    console.print("2. Voice Webhook URL")
    console.print("3. SMS Webhook URL")
    console.print("4. All Settings")
    
    config_choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"])
    
    friendly_name = None
    voice_url = None
    sms_url = None
    
    if config_choice in ["1", "4"]:
        friendly_name = Prompt.ask(
            "Enter new friendly name",
            default=selected_number.get('friendlyName', '')
        )
    
    if config_choice in ["2", "4"]:
        voice_url = Prompt.ask(
            "Enter new voice webhook URL",
            default=selected_number.get('voiceUrl', '')
        )
    
    if config_choice in ["3", "4"]:
        sms_url = Prompt.ask(
            "Enter new SMS webhook URL",
            default=selected_number.get('smsUrl', '')
        )

    # Show summary of changes
    console.print("\n[bold]Review Changes:[/bold]")
    if friendly_name:
        console.print(f"Friendly Name: [red]{selected_number.get('friendlyName', 'N/A')}[/red] → [green]{friendly_name}[/green]")
    if voice_url:
        console.print(f"Voice URL: [red]{selected_number.get('voiceUrl', 'N/A')}[/red] → [green]{voice_url}[/green]")
    if sms_url:
        console.print(f"SMS URL: [red]{selected_number.get('smsUrl', 'N/A')}[/red] → [green]{sms_url}[/green]")

    confirm = Confirm.ask("\n[bold yellow]Apply these changes?[/bold yellow]")
    if not confirm:
        console.print("[yellow]Configuration cancelled.[/yellow]")
        return

    success = configure_number(
        selected_number['sid'],
        friendly_name=friendly_name,
        voice_url=voice_url,
        sms_url=sms_url
    )

    if success:
        console.print(f"[green]✅ Number configured successfully![/green]")
    else:
        console.print(f"[red]❌ Failed to update number settings.[/red]")

    Prompt.ask("\nPress Enter to return")
