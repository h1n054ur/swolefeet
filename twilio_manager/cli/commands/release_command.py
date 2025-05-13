from rich.prompt import Confirm
from rich.table import Table
from twilio_manager.core.phone_numbers import release_number, get_active_numbers
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
    table.add_column("SID", style="yellow")

    for idx, number in enumerate(numbers, 1):
        table.add_row(
            str(idx),
            number['phoneNumber'],
            number.get('friendlyName', 'N/A'),
            number['sid']
        )
    
    console.print(table)

def handle_release_command():
    """Handle the release of a phone number."""
    clear_screen()
    print_header("Release a Phone Number", "🗑")

    # Get list of active numbers
    active_numbers = get_active_numbers()
    
    if not active_numbers:
        print_panel("[yellow]No active numbers found in your account.[/yellow]")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    print_panel("[bold]Active Numbers:[/bold]")
    display_active_numbers(active_numbers)

    # Let user select a number by index
    max_index = len(active_numbers)
    selection = prompt_choice(
        "\nSelect a number to release (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_panel("[yellow]Release cancelled.[/yellow]")
        return

    selected_number = active_numbers[int(selection) - 1]
    confirm = Confirm.ask(
        f"[red]Are you sure you want to release number {selected_number['phoneNumber']}? "
        f"This action is irreversible.[/red]"
    )
    
    if not confirm:
        print_panel("[yellow]Release cancelled.[/yellow]")
        return

    success = release_number(selected_number['sid'])

    if success:
        print_panel(f"[green]✅ Number {selected_number['phoneNumber']} released successfully.[/green]")
    else:
        print_panel(f"[red]❌ Failed to release number {selected_number['phoneNumber']}.[/red]")

    prompt_choice("\nPress Enter to return", choices=[""], default="")
