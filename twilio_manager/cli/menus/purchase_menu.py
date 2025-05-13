from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    print_panel,
    print_success,
    print_error,
    print_warning,
    print_info,
    prompt_choice,
    STYLES
)

class PurchaseMenu(BaseMenu):
    def __init__(self, pre_selected_number=None):
        """Initialize the purchase menu.
        
        Args:
            pre_selected_number (str, optional): Phone number to purchase directly
        """
        self.pre_selected_number = pre_selected_number

    def show(self):
        """Display the purchase menu."""
        if self.pre_selected_number:
            from twilio_manager.cli.commands.purchase_command import confirm_purchase_choice, execute_number_purchase
            
            # Direct purchase flow
            if confirm_purchase_choice(self.pre_selected_number):
                execute_number_purchase(self.pre_selected_number)
            return

        # Search and purchase flow
        options = {
            "1": "Search and purchase a number",
            "0": "Return to previous menu"
        }
        self.display("Purchase Phone Number", "💰", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice == "1":
            from twilio_manager.cli.commands.purchase_command import (
                collect_purchase_parameters,
                search_and_display_numbers,
                confirm_purchase_choice,
                execute_number_purchase
            )
            
            # Get search parameters
            params = collect_purchase_parameters()
            if not params:
                return

            # Search and display numbers
            numbers = search_and_display_numbers(params)
            if not numbers:
                return

            # Get user selection
            selection = prompt_choice(
                "\nSelect a number to purchase (0 to cancel)",
                choices=[str(i) for i in range(len(numbers) + 1)]
            )

            if selection == "0":
                print_warning("Purchase cancelled.")
                return

            # Purchase selected number
            selected_number = numbers[int(selection) - 1]['phoneNumber']
            if confirm_purchase_choice(selected_number):
                execute_number_purchase(selected_number)