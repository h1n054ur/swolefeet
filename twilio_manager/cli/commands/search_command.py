from rich.table import Table
from rich.progress import Progress
from twilio_manager.core.phone_numbers import search_available_numbers
from twilio_manager.shared.ui.styling import (
    console,
    clear_screen,
    print_header,
    print_panel,
    prompt_choice
)

def handle_search_command():
    """Handle the search for available phone numbers."""
    clear_screen()
    print_header("Search Available Numbers", "🔍")

    # Country selection
    print_panel(
        "[bold]Select country:[/bold]\n"
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

    # Number type selection
    print_panel(
        "[bold]Select number type:[/bold]\n"
        "1. Local\n"
        "2. Mobile\n"
        "3. Toll-Free"
    )
    
    type_choice = prompt_choice("Select type", choices=["1", "2", "3"], default="1")
    number_types = {
        "1": "local",
        "2": "mobile",
        "3": "tollfree"
    }
    number_type = number_types[type_choice]

    # Capabilities selection
    print_panel(
        "[bold]Select capabilities:[/bold]\n"
        "1. Voice + SMS\n"
        "2. Voice only\n"
        "3. SMS only\n"
        "4. All (Voice + SMS + MMS)"
    )
    
    caps_choice = prompt_choice("Select capabilities", choices=["1", "2", "3", "4"], default="1")
    capabilities_map = {
        "1": ["VOICE", "SMS"],
        "2": ["VOICE"],
        "3": ["SMS"],
        "4": ["VOICE", "SMS", "MMS"]
    }
    capabilities = capabilities_map[caps_choice]

    # Optional pattern
    print_panel(
        "[bold]Number pattern (optional):[/bold]\n"
        "1. No pattern\n"
        "2. Enter custom pattern"
    )
    
    pattern_choice = prompt_choice("Select option", choices=["1", "2"], default="1")
    pattern = "" if pattern_choice == "1" else prompt_choice("Enter pattern (e.g., 555)", choices=None)

    print_panel("[bold yellow]Searching...[/bold yellow]")

    # Show search criteria
    criteria_summary = (
        "[bold]Search criteria:[/bold]\n"
        f"Country: [cyan]{country_code}[/cyan]\n"
        f"Type: [cyan]{number_type}[/cyan]\n"
        f"Capabilities: [cyan]{', '.join(capabilities)}[/cyan]"
    )
    if pattern:
        criteria_summary += f"\nPattern: [cyan]{pattern}[/cyan]"
    print_panel(criteria_summary)

    # Initialize progress bar
    with Progress() as progress:
        search_task = progress.add_task(
            "[cyan]🔍 Searching for numbers...",
            total=500,
            description="[cyan]Searching"
        )
        
        def update_progress(count):
            progress.update(
                search_task,
                completed=min(count, 500),
                description=f"[cyan]Found {count} numbers"
            )
        
        # Search for numbers with progress tracking
        results, status = search_available_numbers(
            country_code, 
            number_type, 
            capabilities, 
            pattern,
            progress_callback=update_progress
        )

    # Show search status
    if status.startswith("Error"):
        print_panel(f"[red]Search error: {status}[/red]")
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    if not results:
        error_message = (
            "[red]No matching numbers found.[/red]\n\n"
            "Possible reasons:\n"
            "• No numbers available in the selected region\n"
            "• No numbers match the selected capabilities\n"
            "• Pattern too restrictive\n"
            "• Service not available in the selected region\n\n"
            "Try:\n"
            "• Different region\n"
            "• Fewer capabilities\n"
            "• Remove pattern"
        )
        print_panel(error_message)
        prompt_choice("\nPress Enter to return", choices=[""], default="")
        return

    # Show search summary
    print_panel(f"[bold green]{status}[/bold green]")
    
    def display_results_page(page_num: int) -> int:
        """Display a page of search results.
        
        Args:
            page_num (int): The page number to display
            
        Returns:
            int: Total number of pages
        """
        start_idx = (page_num - 1) * 50
        end_idx = min(start_idx + 50, len(results))
        total_pages = (len(results) + 49) // 50  # Round up division
        
        table = Table(
            title=f"[bold]Found {len(results)} Available Numbers (Page {page_num}/{total_pages})[/bold]",
            show_lines=True
        )
        table.add_column("#", style="dim", justify="right")
        table.add_column("Phone Number", style="bold cyan")
        table.add_column("Region", style="green")
        table.add_column("Monthly Cost", style="yellow")
        table.add_column("Capabilities", style="magenta")
        
        for idx, number in enumerate(results[start_idx:end_idx], start_idx + 1):
            # Get capabilities with colors
            caps = []
            if number.get('capabilities', {}).get('voice'):
                caps.append("[blue]VOICE[/blue]")
            if number.get('capabilities', {}).get('sms'):
                caps.append("[green]SMS[/green]")
            if number.get('capabilities', {}).get('mms'):
                caps.append("[yellow]MMS[/yellow]")
            
            # Format price with currency
            price = number.get('monthlyPrice', 0)
            if isinstance(price, (int, float)):
                price_str = f"${price:.2f}"
            else:
                price_str = "—"
            
            # Add row to table
            table.add_row(
                str(idx),
                number.get("phoneNumber", "—"),
                number.get("region", "—"),
                price_str,
                " + ".join(caps) or "—"
            )
        
        console.print("\n")
        console.print(table)
        
        return total_pages
    
    # Handle pagination and purchase options
    current_page = 1
    while True:
        total_pages = display_results_page(current_page)
        
        # Show navigation and purchase options
        options = ["0. Return to menu"]
        if total_pages > 1:
            if current_page > 1:
                options.append("P/p. Previous page")
            if current_page < total_pages:
                options.append("N/n. Next page")
        options.append("\nEnter a number from the list above to purchase")
        
        print_panel("\n[bold]Options:[/bold]\n" + "\n".join(options))
        
        # Build choices list
        choices = ["0"]
        if total_pages > 1:
            if current_page > 1:
                choices.extend(["P", "p"])
            if current_page < total_pages:
                choices.extend(["N", "n"])
        
        # Add number choices for current page but don't show them in prompt
        start_idx = (current_page - 1) * 50
        end_idx = min(start_idx + 50, len(results))
        valid_numbers = [str(i) for i in range(start_idx + 1, end_idx + 1)]
        choices.extend(valid_numbers)
        
        selection = prompt_choice(
            "Select an option",
            choices=choices,
            show_choices=False,
            default="0"
        )
        
        if selection == "0":
            break
        elif selection.upper() == "P" and current_page > 1:
            current_page -= 1
            clear_screen()
            print_header("Search Results", "🔍")
        elif selection.upper() == "N" and current_page < total_pages:
            current_page += 1
            clear_screen()
            print_header("Search Results", "🔍")
        elif selection.isdigit():
            # Handle purchase
            selected_idx = int(selection) - 1
            from twilio_manager.cli.commands.purchase_command import handle_purchase_command
            handle_purchase_command(results[selected_idx]['phoneNumber'])
            break
