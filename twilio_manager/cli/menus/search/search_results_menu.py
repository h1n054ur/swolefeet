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

    def show(self):
        """Display search results with pagination."""
        if not self.results:
            self.handle_empty_result("No phone numbers found matching your criteria.")
            return

        current_page = 1
        while True:
            self.clear()
            self.print_title("Search Results", "📱")
            total_pages = self._display_results_page(current_page)
            
            # Show navigation and purchase options
            self.print_info("\nOptions:")
            self.print_option("0", "Return to menu")
            if total_pages > 1:
                if current_page > 1:
                    self.print_option("P", "Previous page")
                if current_page < total_pages:
                    self.print_option("N", "Next page")
            self.print_info("\nEnter a number from the list above to purchase")
            
            # Build choices list
            choices = ["0"]
            if total_pages > 1:
                if current_page > 1:
                    choices.extend(["P", "p"])
                if current_page < total_pages:
                    choices.extend(["N", "n"])
            
            # Add number choices for current page but don't show them in prompt
            start_idx = (current_page - 1) * 50
            end_idx = min(start_idx + 50, len(self.results))
            valid_numbers = [str(i) for i in range(start_idx + 1, end_idx + 1)]
            choices.extend(valid_numbers)
            
            selection = self.get_choice(
                choices,
                "Select an option",
                "0"
            )
            
            if selection == "0":
                self.return_to_parent()
                return
            elif selection.upper() == "P" and current_page > 1:
                current_page -= 1
            elif selection.upper() == "N" and current_page < total_pages:
                current_page += 1
            elif selection.isdigit():
                # Handle purchase
                selected_idx = int(selection) - 1
                from twilio_manager.cli.commands.purchase_command import handle_purchase_command
                success, error = handle_purchase_command(self.results[selected_idx]['phoneNumber'])
                if success:
                    self.pause_and_return("Phone number purchased successfully!")
                else:
                    self.print_error(f"Failed to purchase number: {error}")
                    self.pause_and_return()
                self.return_to_parent()
                return

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