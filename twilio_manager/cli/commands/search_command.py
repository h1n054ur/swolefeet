from rich.table import Table
from rich.prompt import Prompt, Confirm
from tqdm import tqdm

from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.core.phone_numbers import search_available_numbers

class SearchMenu(BaseMenu):
    def get_title(self):
        return "🔍 Search Available Numbers"

    def get_menu_name(self):
        return "Search Numbers"

    def get_options(self):
        return []  # This menu doesn't use standard options

    def handle_choice(self, choice):
        pass  # Not used in this menu

    def show_search_form(self):
        self.clear_screen()

        # Country selection
        self.console.print("\n[bold]Select country:[/bold]")
        self.print_option("1", "US/Canada (+1)")
        self.print_option("2", "UK (+44)")
        self.print_option("3", "Australia (+61)")
        self.print_option("4", "Other (specify country code)")
        
        country_choice = self.get_choice(["1", "2", "3", "4"], default="1")
        country_codes = {
            "1": "+1",
            "2": "+44",
            "3": "+61"
        }
        
        country_code = country_codes.get(country_choice)
        if country_choice == "4":
            country_code = Prompt.ask("Enter country code (with +)")

        # Number type selection
        self.console.print("\n[bold]Select number type:[/bold]")
        self.print_option("1", "Local")
        self.print_option("2", "Mobile")
        self.print_option("3", "Toll-Free")
        
        type_choice = self.get_choice(["1", "2", "3"], default="1")
        number_types = {
            "1": "local",
            "2": "mobile",
            "3": "tollfree"
        }
        number_type = number_types[type_choice]

        # Capabilities selection
        self.console.print("\n[bold]Select capabilities:[/bold]")
        self.print_option("1", "Voice + SMS")
        self.print_option("2", "Voice only")
        self.print_option("3", "SMS only")
        self.print_option("4", "All (Voice + SMS + MMS)")
        
        caps_choice = self.get_choice(["1", "2", "3", "4"], default="1")
        capabilities_map = {
            "1": ["VOICE", "SMS"],
            "2": ["VOICE"],
            "3": ["SMS"],
            "4": ["VOICE", "SMS", "MMS"]
        }
        capabilities = capabilities_map[caps_choice]

        # Optional pattern
        self.console.print("\n[bold]Number pattern (optional):[/bold]")
        self.print_option("1", "No pattern")
        self.print_option("2", "Enter custom pattern")
        
        pattern_choice = self.get_choice(["1", "2"], default="1")
        pattern = "" if pattern_choice == "1" else Prompt.ask("Enter pattern (e.g., 555)")

        # Show search criteria
        self.console.print("\n[bold]Search criteria:[/bold]")
        self.console.print(f"Country: [cyan]{country_code}[/cyan]")
        self.console.print(f"Type: [cyan]{number_type}[/cyan]")
        self.console.print(f"Capabilities: [cyan]{', '.join(capabilities)}[/cyan]")
        if pattern:
            self.console.print(f"Pattern: [cyan]{pattern}[/cyan]")

        self.console.print("\n[bold yellow]Searching...[/bold yellow]")

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

        return self.show_search_results(results, status)

    def show_search_results(self, results, status):
        # Show search status
        if status.startswith("Error"):
            self.show_error(f"Search error: {status}")
            self.wait_for_input()
            return None

        if not results:
            self.show_error("No matching numbers found.")
            self.console.print("\nPossible reasons:")
            self.console.print("• No numbers available in the selected region")
            self.console.print("• No numbers match the selected capabilities")
            self.console.print("• Pattern too restrictive")
            self.console.print("• Service not available in the selected region")
            self.console.print("\nTry:")
            self.console.print("• Different region")
            self.console.print("• Fewer capabilities")
            self.console.print("• Remove pattern")
            self.wait_for_input()
            return None

        # Show search summary
        self.show_success(status)
        
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
            
            self.console.print("\n")
            self.console.print(table)
            
            return total_pages
        
        # Handle pagination and purchase options
        current_page = 1
        while True:
            self.clear_screen()
            total_pages = display_results_page(current_page)
            
            # Show navigation and purchase options
            self.console.print("\n[bold]Options:[/bold]")
            self.print_option("0", "Return to menu")
            if total_pages > 1:
                if current_page > 1:
                    self.print_option("P", "Previous page")
                if current_page < total_pages:
                    self.print_option("N", "Next page")
            self.console.print("\nEnter a number from the list above to purchase")
            
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
            
            selection = self.get_choice(choices, show_choices=False, default="0")
            
            if selection == "0":
                return None
            elif selection.upper() == "P" and current_page > 1:
                current_page -= 1
            elif selection.upper() == "N" and current_page < total_pages:
                current_page += 1
            elif selection.isdigit():
                # Return the selected number for purchase
                selected_idx = int(selection) - 1
                return results[selected_idx]['phoneNumber']

def handle_search_command():
    menu = SearchMenu()
    selected_number = menu.show_search_form()
    if selected_number:
        from twilio_manager.cli.commands.purchase_command import handle_purchase_command
        handle_purchase_command(selected_number)