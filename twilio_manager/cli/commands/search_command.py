from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from tqdm import tqdm

from twilio_manager.core.phone_numbers import search_available_numbers

console = Console()

def handle_search_command():
    console.clear()
    console.print(Panel.fit("[bold cyan]🔍 Search Available Numbers[/bold cyan]"))

    # Country selection
    console.print("\n[bold]Select country:[/bold]")
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

    # Use tqdm for a simulated loading experience
    with tqdm(total=1, desc="🔍 Fetching numbers", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        results = search_available_numbers(country_code, number_type, capabilities, pattern)
        pbar.update(1)

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

    table = Table(title=f"[bold]Found {len(results)} Available Numbers[/bold]", show_lines=True)
    table.add_column("#", style="dim", justify="right")
    table.add_column("Phone Number", style="bold cyan")
    table.add_column("Region", style="green")
    table.add_column("Monthly Cost", style="yellow")
    table.add_column("Capabilities", style="magenta")

    for idx, number in enumerate(results, 1):
        # Get capabilities
        caps = []
        if number.get('capabilities', {}).get('voice'):
            caps.append("[blue]VOICE[/blue]")
        if number.get('capabilities', {}).get('sms'):
            caps.append("[green]SMS[/green]")
        if number.get('capabilities', {}).get('mms'):
            caps.append("[yellow]MMS[/yellow]")

        # Format price
        price = number.get('monthlyPrice', 0)
        if isinstance(price, (int, float)):
            price_str = f"${price:.2f}"
        else:
            price_str = "—"

        table.add_row(
            str(idx),
            number.get("phoneNumber", "—"),
            number.get("region", "—"),
            price_str,
            " + ".join(caps) or "—"
        )

    console.print("\n")
    console.print(table)
    
    # Option to purchase
    console.print("\n[bold]Would you like to purchase one of these numbers?[/bold]")
    console.print("0. No, return to menu")
    console.print("1-N. Select number to purchase")
    
    max_index = len(results)
    selection = Prompt.ask(
        "Select an option",
        choices=[str(i) for i in range(max_index + 1)],
        default="0"
    )
    
    if selection != "0":
        from twilio_manager.cli.commands.purchase_command import handle_purchase_command
        selected_number = results[int(selection) - 1]
        handle_purchase_command(selected_number['phoneNumber'])
    else:
        Prompt.ask("\nPress Enter to return")
