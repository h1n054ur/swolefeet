from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from twilio_manager.core.phone_numbers import purchase_number, search_available_numbers

console = Console()

def display_number_options(numbers):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim")
    table.add_column("Phone Number", style="cyan")
    table.add_column("Region", style="green")
    table.add_column("Monthly Cost", style="yellow")

    for idx, number in enumerate(numbers, 1):
        table.add_row(
            str(idx),
            number['phoneNumber'],
            f"{number.get('region', 'N/A')}",
            f"${number.get('monthlyPrice', 'N/A')}"
        )
    
    console.print(table)

def handle_purchase_command(pre_selected_number=None):
    """
    Handle the purchase of a phone number.
    
    Args:
        pre_selected_number: Optional phone number to purchase directly
    """
    console.clear()
    console.print(Panel.fit("[bold cyan]🛒 Purchase a Phone Number[/bold cyan]"))

    if pre_selected_number:
        # If number is pre-selected (e.g., from search), confirm and purchase
        confirm = Confirm.ask(f"Are you sure you want to purchase [bold green]{pre_selected_number}[/bold green]?")
        
        if not confirm:
            console.print("[yellow]Purchase cancelled.[/yellow]")
            return

        success = purchase_number(pre_selected_number)

        if success:
            console.print(f"[green]✅ Number {pre_selected_number} purchased successfully![/green]")
        else:
            console.print(f"[red]❌ Failed to purchase number {pre_selected_number}.[/red]")

        Prompt.ask("\nPress Enter to return")
        return

    # If no pre-selected number, show search interface
    console.print("\n[bold]Search for available numbers:[/bold]")
    console.print("1. US/Canada (+1)")
    console.print("2. UK (+44)")
    console.print("3. Australia (+61)")
    console.print("4. Other (specify country code)")

    country_choice = Prompt.ask("Select country", choices=["1", "2", "3", "4"], default="1")
    country_codes = {
        "1": "+1",
        "2": "+44",
        "3": "+61"
    }
    
    country_code = country_codes.get(country_choice)
    if country_choice == "4":
        country_code = Prompt.ask("Enter country code (with +)")

    # Search for available numbers
    available_numbers = search_available_numbers(country_code)
    
    if not available_numbers:
        console.print("[red]No numbers available in the selected region.[/red]")
        Prompt.ask("\nPress Enter to return")
        return

    console.print("\n[bold]Available Numbers:[/bold]")
    display_number_options(available_numbers)

    # Let user select a number by index
    max_index = len(available_numbers)
    selection = Prompt.ask(
        "\nSelect a number to purchase (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        console.print("[yellow]Purchase cancelled.[/yellow]")
        return

    selected_number = available_numbers[int(selection) - 1]['phoneNumber']
    confirm = Confirm.ask(f"Are you sure you want to purchase [bold green]{selected_number}[/bold green]?")
    
    if not confirm:
        console.print("[yellow]Purchase cancelled.[/yellow]")
        return

    success = purchase_number(selected_number)

    if success:
        console.print(f"[green]✅ Number {selected_number} purchased successfully![/green]")
    else:
        console.print(f"[red]❌ Failed to purchase number {selected_number}.[/red]")

    Prompt.ask("\nPress Enter to return")
