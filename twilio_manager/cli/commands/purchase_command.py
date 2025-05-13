from rich.prompt import Confirm
from rich.table import Table
from twilio_manager.core.phone_numbers import purchase_number, search_available_numbers
from twilio_manager.shared.ui.styling import (
    console,
    clear_screen,
    print_header,
    print_panel,
    prompt_choice
)

def display_number_options(numbers):
    """Display a table of available phone numbers.
    
    Args:
        numbers (list): List of phone number dictionaries
    """
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
    """Handle the purchase of a phone number.
    
    Args:
        pre_selected_number (str, optional): Phone number to purchase directly
    """
    clear_screen()
    print_header("Purchase a Phone Number", "🛒")

    if pre_selected_number:
        # If number is pre-selected (e.g., from search), confirm and purchase
        confirm = Confirm.ask(f"Are you sure you want to purchase [bold green]{pre_selected_number}[/bold green]?")
        
        if not confirm:
            print_panel("[yellow]Purchase cancelled.[/yellow]")
            return

        success = purchase_number(pre_selected_number)

        if success:
            print_panel(f"[green]✅ Number {pre_selected_number} purchased successfully![/green]")
        else:
            print_panel(f"[red]❌ Failed to purchase number {pre_selected_number}.[/red]")

        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    # If no pre-selected number, show search interface
    print_panel(
        "[bold]Search for available numbers:[/bold]\n"
        "1. US/Canada (+1)\n"
        "2. UK (+44)\n"
        "3. Australia (+61)\n"
        "4. Other (specify country code)"
    )

    country_choice = prompt_choice("Select country", choices=["1", "2", "3", "4"], default="1")
    country_codes = {
        "1": "+1",
        "2": "+44",
        "3": "+61"
    }
    
    country_code = country_codes.get(country_choice)
    if country_choice == "4":
        country_code = prompt_choice("Enter country code (with +)", choices=None)

    # Search for available numbers
    available_numbers = search_available_numbers(country_code)
    
    if not available_numbers:
        print_panel("[red]No numbers available in the selected region.[/red]")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    print_panel("[bold]Available Numbers:[/bold]")
    display_number_options(available_numbers)

    # Let user select a number by index
    max_index = len(available_numbers)
    selection = prompt_choice(
        "\nSelect a number to purchase (0 to cancel)",
        choices=[str(i) for i in range(max_index + 1)]
    )

    if selection == "0":
        print_panel("[yellow]Purchase cancelled.[/yellow]")
        return

    selected_number = available_numbers[int(selection) - 1]['phoneNumber']
    confirm = Confirm.ask(f"Are you sure you want to purchase [bold green]{selected_number}[/bold green]?")
    
    if not confirm:
        print_panel("[yellow]Purchase cancelled.[/yellow]")
        return

    success = purchase_number(selected_number)

    if success:
        print_panel(f"[green]✅ Number {selected_number} purchased successfully![/green]")
    else:
        print_panel(f"[red]❌ Failed to purchase number {selected_number}.[/red]")

    prompt_choice("\nPress Enter to return", choices=[""], default="")
