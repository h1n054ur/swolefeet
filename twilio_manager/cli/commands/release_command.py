from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from twilio_manager.core.phone_numbers import release_number, get_active_numbers

console = Console()

def display_active_numbers(numbers):
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
    console.clear()
    console.print(Panel.fit("[bold cyan]🗑 Release a Phone Number[/bold cyan]"))

    # Get list of active numbers
    active_numbers = get_active_numbers()
    
    if not active_numbers:
        console.print("[yellow]No active numbers found in your account.[/yellow]")
        Prompt.ask("\nPress Enter to return")
        return

    console.print("\n[bold]Active Numbers:[/bold]")
    display_active_numbers(active_numbers)

    # Let user select a number by index
    max_index = len(active_numbers)
    selection = Prompt.ask(
        "\nSelect a number to release (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        console.print("[yellow]Release cancelled.[/yellow]")
        return

    selected_number = active_numbers[int(selection) - 1]
    confirm = Confirm.ask(
        f"[red]Are you sure you want to release number {selected_number['phoneNumber']}? "
        f"This action is irreversible.[/red]"
    )
    
    if not confirm:
        console.print("[yellow]Release cancelled.[/yellow]")
        return

    success = release_number(selected_number['sid'])

    if success:
        console.print(f"[green]✅ Number {selected_number['phoneNumber']} released successfully.[/green]")
    else:
        console.print(f"[red]❌ Failed to release number {selected_number['phoneNumber']}.[/red]")

    Prompt.ask("\nPress Enter to return")
