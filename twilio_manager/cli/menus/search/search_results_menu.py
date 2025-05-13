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
from twilio_manager.shared.utils.logger import get_logger

logger = get_logger(__name__)

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

        current_page = 1
        while True:
            try:
                self.clear()
                self.print_title("Search Results", "📱")
                total_pages = self._display_results_page(current_page)
                
                # Show navigation and purchase options
                self.print_info("Options:")
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
                    break
                elif selection.upper() == "P" and current_page > 1:
                    current_page -= 1
                elif selection.upper() == "N" and current_page < total_pages:
                    current_page += 1
                elif selection.isdigit():
                    # Handle purchase
                    selected_idx = int(selection) - 1
                    if 0 <= selected_idx < len(self.results):
                        from twilio_manager.cli.commands.purchase_command import handle_purchase_command
                        success, error = handle_purchase_command(self.results[selected_idx]['phoneNumber'])
                        if success:
                            self.pause_and_return("Phone number purchased successfully!")
                        else:
                            self.print_error(f"Failed to purchase number: {error}")
                            self.pause_and_return()
                        break
                    else:
                        self.print_error("Invalid selection")
                        continue
                
            except Exception as e:
                logger.error(f"Error in search results menu: {str(e)}", exc_info=True)
                self.print_error("An error occurred. Please try again.")
                self.pause_and_return()
                break

    def _display_results_page(self, page_num: int) -> int:
        """Display a page of search results.
        
        Args:
            page_num (int): The page number to display
            
        Returns:
            int: Total number of pages
        """
        try:
            start_idx = (page_num - 1) * 50
            end_idx = min(start_idx + 50, len(self.results))
            total_pages = (len(self.results) + 49) // 50  # Round up division
            
            # Get terminal width and adjust table accordingly
            width = console.width or 80
            
            # Create table with dynamic width
            table = create_table(
                columns=["#", "Phone Number", "Region", "Monthly Cost", "Capabilities"],
                title=f"Found {len(self.results)} Available Numbers (Page {page_num}/{total_pages})",
                width=min(width - 2, 120)  # Leave some margin
            )
            
            # Set column widths based on content and terminal width
            number_width = max(len(str(end_idx)), 3)
            phone_width = 15
            region_width = min(20, max(10, (width - number_width - phone_width - 25) // 3))
            price_width = 12
            caps_width = width - number_width - phone_width - region_width - price_width - 10
            
            table.columns[0].width = number_width
            table.columns[1].width = phone_width
            table.columns[2].width = region_width
            table.columns[3].width = price_width
            table.columns[4].width = caps_width
            
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
                
                # Format region to fit
                region = number.get("region", "—")
                if len(region) > region_width:
                    region = region[:region_width-3] + "..."
                
                # Format capabilities to fit
                caps_str = " + ".join(caps) or "—"
                if len(caps_str) > caps_width:
                    caps_str = caps_str[:caps_width-3] + "..."
                
                # Add row to table
                table.add_row(
                    str(idx),
                    number.get("phoneNumber", "—"),
                    region,
                    price_str,
                    caps_str,
                    style=STYLES['data']
                )
            
            # Clear screen and print table
            console.clear()
            console.print("\n")
            console.print(table)
            
            return total_pages
            
        except Exception as e:
            logger.error(f"Error displaying results page: {str(e)}", exc_info=True)
            self.print_error("Error displaying results. Please try again.")
            return total_pages

    def handle_empty_result(self, message):
        """Handle case when no results are found.
        
        Args:
            message (str): Message to display to user
        """
        self.clear()
        self.print_title("No Results", "❌")
        print_panel(message, style='error')
        self.print_info("\nPossible reasons:")
        console.print("• No numbers available in the selected region", style=STYLES['data'])
        console.print("• No numbers match the selected capabilities", style=STYLES['data'])
        console.print("• Pattern too restrictive", style=STYLES['data'])
        console.print("• Service not available in the selected region", style=STYLES['data'])
        
        self.print_info("\nTry:")
        console.print("• Different region", style=STYLES['data'])
        console.print("• Fewer capabilities", style=STYLES['data'])
        console.print("• Remove pattern", style=STYLES['data'])
        
        self.pause_and_return()