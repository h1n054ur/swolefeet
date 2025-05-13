from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from tqdm import tqdm

from twilio_manager.cli.menus.base_menu import BaseMenu, SearchResultsMenu
from twilio_manager.core.phone_numbers import search_available_numbers

class SearchCriteriaMenu(BaseMenu):
    def __init__(self):
        super().__init__("Search Available Numbers", "🔍")
        self.country_code = None
        self.number_type = None
        self.capabilities = None
        self.pattern = None

    def get_country_code(self):
        self.console.print("\n[bold]Select country:[/bold]")
        self.console.print("1. US/Canada (+1)")
        self.console.print("2. UK (+44)")
        self.console.print("3. Australia (+61)")
        self.console.print("4. Other (specify country code)")
        
        country_choice = Prompt.ask("Select country", choices=["1", "2", "3", "4"], default="1")
        country_codes = {
            "1": "+1",
            "2": "+44",
            "3": "+61"
        }
        
        self.country_code = country_codes.get(country_choice)
        if country_choice == "4":
            self.country_code = Prompt.ask("Enter country code (with +)")

    def get_number_type(self):
        self.console.print("\n[bold]Select number type:[/bold]")
        self.console.print("1. Local")
        self.console.print("2. Mobile")
        self.console.print("3. Toll-Free")
        
        type_choice = Prompt.ask("Select type", choices=["1", "2", "3"], default="1")
        number_types = {
            "1": "local",
            "2": "mobile",
            "3": "tollfree"
        }
        self.number_type = number_types[type_choice]

    def get_capabilities(self):
        self.console.print("\n[bold]Select capabilities:[/bold]")
        self.console.print("1. Voice + SMS")
        self.console.print("2. Voice only")
        self.console.print("3. SMS only")
        self.console.print("4. All (Voice + SMS + MMS)")
        
        caps_choice = Prompt.ask("Select capabilities", choices=["1", "2", "3", "4"], default="1")
        capabilities_map = {
            "1": ["VOICE", "SMS"],
            "2": ["VOICE"],
            "3": ["SMS"],
            "4": ["VOICE", "SMS", "MMS"]
        }
        self.capabilities = capabilities_map[caps_choice]

    def get_pattern(self):
        self.console.print("\n[bold]Number pattern (optional):[/bold]")
        self.console.print("1. No pattern")
        self.console.print("2. Enter custom pattern")
        
        pattern_choice = Prompt.ask("Select option", choices=["1", "2"], default="1")
        self.pattern = "" if pattern_choice == "1" else Prompt.ask("Enter pattern (e.g., 555)")

    def show_criteria(self):
        self.console.print("\n[bold]Search criteria:[/bold]")
        self.console.print(f"Country: [cyan]{self.country_code}[/cyan]")
        self.console.print(f"Type: [cyan]{self.number_type}[/cyan]")
        self.console.print(f"Capabilities: [cyan]{', '.join(self.capabilities)}[/cyan]")
        if self.pattern:
            self.console.print(f"Pattern: [cyan]{self.pattern}[/cyan]")

    def show(self):
        self.clear_screen()
        self.show_title()
        
        self.get_country_code()
        self.get_number_type()
        self.get_capabilities()
        self.get_pattern()

        self.console.print("\n[bold yellow]Searching...[/bold yellow]")
        self.show_criteria()

        # Initialize progress bar
        with tqdm(total=500, desc="🔍 Searching for numbers", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} numbers") as pbar:
            def update_progress(count):
                pbar.n = min(count, 500)
                pbar.refresh()
            
            # Search for numbers with progress tracking
            results, status = search_available_numbers(
                self.country_code, 
                self.number_type, 
                self.capabilities, 
                self.pattern,
                progress_callback=update_progress
            )

        if status.startswith("Error"):
            self.console.print(f"\n[red]Search error: {status}[/red]")
            Prompt.ask("\nPress Enter to return")
            return None

        if not results:
            self.console.print("\n[red]No matching numbers found.[/red]")
            self.console.print("\nPossible reasons:")
            self.console.print("• No numbers available in the selected region")
            self.console.print("• No numbers match the selected capabilities")
            self.console.print("• Pattern too restrictive")
            self.console.print("• Service not available in the selected region")
            self.console.print("\nTry:")
            self.console.print("• Different region")
            self.console.print("• Fewer capabilities")
            self.console.print("• Remove pattern")
            Prompt.ask("\nPress Enter to return")
            return None

        self.console.print(f"\n[bold green]{status}[/bold green]")
        return results

class PhoneNumberResultsMenu(SearchResultsMenu):
    def __init__(self, results):
        super().__init__("Search Results", results)

    def display_results_page(self):
        start_idx = (self.current_page - 1) * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.results))
        
        table = Table(
            title=f"[bold]Found {len(self.results)} Available Numbers (Page {self.current_page}/{self.total_pages})[/bold]",
            show_lines=True
        )
        table.add_column("#", style="dim", justify="right")
        table.add_column("Phone Number", style="bold cyan")
        table.add_column("Region", style="green")
        table.add_column("Monthly Cost", style="yellow")
        table.add_column("Capabilities", style="magenta")
        
        for idx, number in enumerate(self.results[start_idx:end_idx], start_idx + 1):
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
        
        self.console.print("\n")
        self.console.print(table)

        # Show navigation options
        self.console.print("\n[bold]Options:[/bold]")
        self.console.print("0. Return to menu")
        if self.total_pages > 1:
            if self.current_page > 1:
                self.console.print("P/p. Previous page")
            if self.current_page < self.total_pages:
                self.console.print("N/n. Next page")
        self.console.print("\nEnter a number from the list above to purchase")

    def handle_item_selection(self, index: int) -> bool:
        from twilio_manager.cli.commands.purchase_command import handle_purchase_command
        handle_purchase_command(self.results[index]['phoneNumber'])
        return True

def handle_search_command():
    search_menu = SearchCriteriaMenu()
    results = search_menu.show()
    
    if results:
        results_menu = PhoneNumberResultsMenu(results)
        results_menu.show()
    
    return False  # Don't exit the parent menu
