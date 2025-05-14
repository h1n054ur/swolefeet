from rich.progress import Progress
from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_panel,
    print_success,
    print_error,
    print_warning,
    print_info,
    prompt_choice,
    STYLES
)

class SearchResultsMenu(BaseMenu):
    def __init__(self, results, status, parent=None):
        """Initialize search results menu.
        
        Args:
            results (list): List of phone number results
            status (str): Search status message
            parent (BaseMenu, optional): Parent menu to return to
        """
        super().__init__(parent)
        self.results = results
        self.status = status
        self.current_page = 1
        self.total_pages = (len(results) + 49) // 50 if results else 0  # Round up division

    def show(self):
        """Display search results with pagination."""
        if not self.results:
            self.handle_empty_result("No phone numbers found matching your criteria.")
            return

        self._show_current_page()
        return None

    def _show_current_page(self):
        """Show the current page of results."""
        total_pages = self._display_results_page(self.current_page)
        
        options = {"0": "Return to menu"}
        
        # Add navigation options
        if total_pages > 1:
            if self.current_page > 1:
                options["P"] = "Previous page"
            if self.current_page < total_pages:
                options["N"] = "Next page"
        
        # Add purchase options (hidden from display but valid choices)
        start_idx = (self.current_page - 1) * 50
        end_idx = min(start_idx + 50, len(self.results))
        for i in range(start_idx + 1, end_idx + 1):
            options[str(i)] = ""  # Hidden option
            
        self.display(
            title=f"Search Results (Page {self.current_page}/{total_pages})",
            emoji="📱",
            options=options
        )

    def handle_choice(self, choice):
        """Handle menu selection."""
        choice = choice.upper()
        
        if choice == "P" and self.current_page > 1:
            self.current_page -= 1
            self._show_current_page()
        elif choice == "N" and self.current_page < self.total_pages:
            self.current_page += 1
            self._show_current_page()
        elif choice.isdigit():
            selected_idx = int(choice) - 1
            if 0 <= selected_idx < len(self.results):
                self._handle_purchase(selected_idx)
            else:
                self.print_error("Invalid selection")
                self.pause_and_return()

    def _handle_purchase(self, selected_idx):
        """Handle phone number purchase."""
        from twilio_manager.cli.commands.purchase_command import handle_purchase_command
        number = self.results[selected_idx]['phoneNumber']
        
        self.print_info(f"\nAttempting to purchase {number}...")
        success, error = handle_purchase_command(number)
        
        if success:
            self.print_success("Phone number purchased successfully!")
            self.pause_and_return()
        else:
            self.print_error(f"Failed to purchase number: {error}")
            self.pause_and_return()

    def _display_results_page(self, page_num: int) -> int:
        """Display a page of search results.
        
        Args:
            page_num (int): The page number to display
            
        Returns:
            int: Total number of pages
        """
        start_idx = (page_num - 1) * 50
        end_idx = min(start_idx + 50, len(self.results))
        total_pages = (len(self.results) + 49) // 50  # Round up division
        
        table = create_table(
            columns=["#", "Phone Number", "Region", "Monthly Cost", "Capabilities"],
            title=f"Found {len(self.results)} Available Numbers (Page {page_num}/{total_pages})"
        )
        
        for idx, number in enumerate(self.results[start_idx:end_idx], start_idx + 1):
            # Get capabilities
            caps = []
            if number.get('capabilities', {}).get('voice'):
                caps.append("VOICE")
            if number.get('capabilities', {}).get('sms'):
                caps.append("SMS")
            if number.get('capabilities', {}).get('mms'):
                caps.append("MMS")
            
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
                " + ".join(caps) or "—",
                style=STYLES['data']
            )
        
        console.print("\n")
        console.print(table)
        
        return total_pages