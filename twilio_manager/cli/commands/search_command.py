from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from tqdm import tqdm

from twilio_manager.core.phone_numbers import search_available_numbers

console = Console()

def handle_search_command():
    # Country selection
    console.print("[bold]Select country:[/bold]")
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

    # Number type selection
    console.print("\n[bold]Select number type:[/bold]")
    console.print("1. Local")
    console.print("2. Mobile")
    console.print("3. Toll-Free")
    
    type_choice = Prompt.ask("Select type", choices=["1", "2", "3"], default="1")
    number_types = {
        "1": "local",
        "2": "mobile",
        "3": "tollfree"
    }
    number_type = number_types[type_choice]

    # Capabilities selection
    console.print("\n[bold]Select capabilities:[/bold]")
    console.print("1. Voice + SMS")
    console.print("2. Voice only")
    console.print("3. SMS only")
    console.print("4. All (Voice + SMS + MMS)")
    
    caps_choice = Prompt.ask("Select capabilities", choices=["1", "2", "3", "4"], default="1")
    capabilities_map = {
        "1": ["VOICE", "SMS"],
        "2": ["VOICE"],
        "3": ["SMS"],
        "4": ["VOICE", "SMS", "MMS"]
    }
    capabilities = capabilities_map[caps_choice]

    # Optional pattern
    console.print("\n[bold]Number pattern (optional):[/bold]")
    console.print("1. No pattern")
    console.print("2. Enter custom pattern")
    
    pattern_choice = Prompt.ask("Select option", choices=["1", "2"], default="1")
    pattern = "" if pattern_choice == "1" else Prompt.ask("Enter pattern (e.g., 555)")

    console.print("\n[bold yellow]Searching...[/bold yellow]")

    # Show search criteria
    console.print("\n[bold]Search criteria:[/bold]")
    console.print(f"Country: [cyan]{country_code}[/cyan]")
    console.print(f"Type: [cyan]{number_type}[/cyan]")
    console.print(f"Capabilities: [cyan]{', '.join(capabilities)}[/cyan]")
    if pattern:
        console.print(f"Pattern: [cyan]{pattern}[/cyan]")

    # Show search criteria
    console.print("\n[bold]Search criteria:[/bold]")
    console.print(f"Country: [cyan]{country_code}[/cyan]")
    console.print(f"Type: [cyan]{number_type}[/cyan]")
    console.print(f"Capabilities: [cyan]{', '.join(capabilities)}[/cyan]")
    if pattern:
        console.print(f"Pattern: [cyan]{pattern}[/cyan]")

    # Initialize progress bar
    with tqdm(total=500, desc="🔍 Searching for numbers", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} numbers") as pbar:
        def update_progress(count):
            pbar.n = min(count, 500)
            pbar.refresh()
        
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
        console.print(f"\n[red]Search error: {status}[/red]")
        Prompt.ask("\nPress Enter to return")
        return

    if not results:
        console.print("\n[red]No matching numbers found.[/red]")
        console.print("\nPossible reasons:")
        console.print("• No numbers available in the selected region")
        console.print("• No numbers match the selected capabilities")
        console.print("• Pattern too restrictive")
        console.print("• Service not available in the selected region")
        console.print("\nTry:")
        console.print("• Different region")
        console.print("• Fewer capabilities")
        console.print("• Remove pattern")
        Prompt.ask("\nPress Enter to return")
        return

    # Show search summary
    console.print(f"\n[bold green]{status}[/bold green]")
    
    def display_results_page(page_num: int) -> int:
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
        console.print("\n[bold]Options:[/bold]")
        console.print("0. Return to menu")
        if total_pages > 1:
            if current_page > 1:
                console.print("P/p. Previous page")
            if current_page < total_pages:
                console.print("N/n. Next page")
        console.print("\nEnter a number from the list above to purchase")
        
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
        
        selection = Prompt.ask(
            "Select an option",
            choices=choices,
            show_choices=False,
            default="0"
        )
        
        if selection == "0":
            break
        elif selection.upper() == "P" and current_page > 1:
            current_page -= 1
        elif selection.upper() == "N" and current_page < total_pages:
            current_page += 1
        elif selection.isdigit():
            # Handle purchase
            selected_idx = int(selection) - 1
            from twilio_manager.cli.commands.purchase_command import handle_purchase_command
            handle_purchase_command(results[selected_idx]['phoneNumber'])
            break
