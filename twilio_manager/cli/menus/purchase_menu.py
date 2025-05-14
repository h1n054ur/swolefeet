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
        self.clear()
        self.print_title("Select Country", "🌎")
        self.print_option("1", "US/Canada (+1)")
        self.print_option("2", "UK (+44)")
        self.print_option("3", "Australia (+61)")
        self.print_option("4", "Other (specify country code)")

        country_choice = self.get_choice(["1", "2", "3", "4"], "Select country", "1")
        country_codes = get_country_codes()
        
        country_code = country_codes.get(country_choice)
        if country_choice == "4":
            country_code = self.get_choice(None, "Enter country code (with +)")

        return country_code

class AvailableNumbersMenu(BaseMenu):
    def __init__(self, available_numbers):
        """Initialize the menu.
        
        Args:
            available_numbers (list): List of available phone numbers
        """
        super().__init__()
        self.available_numbers = available_numbers

    def show(self):
        """Display available numbers and get user selection."""
        self.clear()
        self.print_title("Available Numbers", "📱")

        table = create_table(columns=["#", "Phone Number", "Region", "Monthly Cost"])
        for idx, number in enumerate(self.available_numbers, 1):
            table.add_row(
                str(idx),
                number['phoneNumber'],
                f"{number.get('region', 'N/A')}",
                f"${number.get('monthlyPrice', 'N/A')}",
                style=STYLES['data']
            )
        console.print(table)

        # Get user selection
        selection = self.get_choice(
            [str(i) for i in range(len(self.available_numbers) + 1)],
            "\nSelect a number to purchase (0 to cancel)"
        )

        if selection == "0":
            self.print_warning("Purchase cancelled.")
            return None

        return self.available_numbers[int(selection) - 1]['phoneNumber']

class PurchaseConfirmationMenu(BaseMenu):
    def __init__(self, phone_number):
        """Initialize the menu.
        
        Args:
            phone_number (str): Phone number to purchase
        """
        super().__init__()
        self.phone_number = phone_number

    def show(self):
        """Display purchase confirmation menu."""
        self.clear()
        self.print_title("Confirm Purchase", "💰")
        
        if not confirm_action(f"Are you sure you want to purchase {self.phone_number}?"):
            self.print_warning("Purchase cancelled.")
            return False

        success, error = purchase_phone_number(self.phone_number)

        if success:
            self.print_success(f"Number {self.phone_number} purchased successfully!")
        else:
            error_msg = error or "Unknown error"
            self.print_error(f"Failed to purchase number {self.phone_number}: {error_msg}")

        self.get_choice([""], "\nPress Enter to return", "")
        return success

class PurchaseMenu(BaseMenu):
    def __init__(self, pre_selected_number=None):
        """Initialize the purchase menu.
        
        Args:
            pre_selected_number (str, optional): Phone number to purchase directly
        """
        super().__init__()
        self.pre_selected_number = pre_selected_number

    def show(self):
        """Display the purchase menu and handle purchase flow."""
        if self.pre_selected_number:
            # Direct purchase flow
            PurchaseConfirmationMenu(self.pre_selected_number).show()
            return

        # Search and purchase flow
        country_code = SelectCountryMenu().show()
        if not country_code:
            return

        # Search for numbers
        self.print_info("Searching...")
        available_numbers = search_available_numbers_by_country(country_code)
        
        if not available_numbers:
            self.clear()
            self.print_title("No Numbers Found", "❌")
            self.print_error("No numbers available in the selected region.")
            self.get_choice([""], "\nPress Enter to return", "")
            return

        # Show available numbers and get selection
        selected_number = AvailableNumbersMenu(available_numbers).show()
        if not selected_number:
            return

        # Confirm and execute purchase
        PurchaseConfirmationMenu(selected_number).show()