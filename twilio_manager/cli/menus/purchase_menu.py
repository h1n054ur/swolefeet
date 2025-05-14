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
    confirm_action,
    STYLES
)
from twilio_manager.cli.commands.purchase_command import (
    get_country_codes,
    search_available_numbers_by_country,
    purchase_phone_number
)

class SelectCountryMenu(BaseMenu):
    def show(self):
        """Display country selection menu."""
        self.display("Select Country", "🌎", {
            "1": "US/Canada (+1)",
            "2": "UK (+44)",
            "3": "Australia (+61)",
            "4": "Other (specify country code)",
            "0": "Back"
        })

    def handle_choice(self, choice):
        """Handle country selection.
        
        Args:
            choice (str): The user's selected option
        """
        country_codes = get_country_codes()
        country_code = country_codes.get(choice)
        
        if choice == "4":
            country_code = self.get_choice(None, "Enter country code (with +)")
            if not country_code:
                return
        
        if country_code:
            # Search for numbers
            self.print_info("Searching...")
            available_numbers = search_available_numbers_by_country(country_code)
            
            if not available_numbers:
                self.print_error("No numbers available in the selected region.")
                self.pause_and_return()
                return
            
            # Show available numbers menu
            AvailableNumbersMenu(self, available_numbers).show()

class AvailableNumbersMenu(BaseMenu):
    def __init__(self, parent=None, available_numbers=None):
        """Initialize the menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu
            available_numbers (list): List of available phone numbers
        """
        super().__init__(parent)
        self.available_numbers = available_numbers or []

    def show(self):
        """Display available numbers menu."""
        # Create options dictionary
        options = {}
        for idx, number in enumerate(self.available_numbers, 1):
            region = number.get('region', 'N/A')
            price = number.get('monthlyPrice', 'N/A')
            options[str(idx)] = f"{number['phoneNumber']} ({region}) - ${price}/mo"
        options["0"] = "Back"

        self.display("Available Numbers", "📱", options)

    def handle_choice(self, choice):
        """Handle number selection.
        
        Args:
            choice (str): The user's selected option
        """
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(self.available_numbers):
            return
            
        selected_number = self.available_numbers[int(choice) - 1]['phoneNumber']
        PurchaseConfirmationMenu(self, selected_number).show()

class PurchaseConfirmationMenu(BaseMenu):
    def __init__(self, parent=None, phone_number=None):
        """Initialize the menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu
            phone_number (str): Phone number to purchase
        """
        super().__init__(parent)
        self.phone_number = phone_number

    def show(self):
        """Display purchase confirmation menu."""
        self.display("Confirm Purchase", "💰", {
            "1": f"Purchase {self.phone_number}",
            "0": "Cancel"
        })

    def handle_choice(self, choice):
        """Handle purchase confirmation.
        
        Args:
            choice (str): The user's selected option
        """
        if choice != "1":
            return

        if not confirm_action(f"Are you sure you want to purchase {self.phone_number}?"):
            self.print_warning("Purchase cancelled.")
            self.pause_and_return()
            return

        success, error = purchase_phone_number(self.phone_number)

        if success:
            self.print_success(f"Number {self.phone_number} purchased successfully!")
        else:
            error_msg = error or "Unknown error"
            self.print_error(f"Failed to purchase number {self.phone_number}: {error_msg}")

        self.pause_and_return()

class PurchaseMenu(BaseMenu):
    def __init__(self, parent=None, pre_selected_number=None):
        """Initialize the purchase menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu
            pre_selected_number (str, optional): Phone number to purchase directly
        """
        super().__init__(parent)
        self.pre_selected_number = pre_selected_number

    def show(self):
        """Display the purchase menu."""
        if self.pre_selected_number:
            # Direct purchase flow
            PurchaseConfirmationMenu(self, self.pre_selected_number).show()
            return

        # Show country selection menu
        SelectCountryMenu(self).show()

    def handle_choice(self, choice):
        """Handle menu choice.
        
        Args:
            choice (str): The user's selected option
        """
        pass  # All handling done in show() since this is just a router menu