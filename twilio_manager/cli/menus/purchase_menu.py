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

class PurchaseMenu(BaseMenu):
    def __init__(self, pre_selected_number=None):
        """Initialize the purchase menu.
        
        Args:
            pre_selected_number (str, optional): Phone number to purchase directly
        """
        self.pre_selected_number = pre_selected_number

    def show(self):
        """Display the purchase menu and handle purchase flow."""
        if self.pre_selected_number:
            # Direct purchase flow
            if self._confirm_purchase(self.pre_selected_number):
                self._execute_purchase(self.pre_selected_number)
            return

        # Search and purchase flow
        print_panel("Search for available numbers:", style='highlight')
        console.print("1. US/Canada (+1)", style=STYLES['data'])
        console.print("2. UK (+44)", style=STYLES['data'])
        console.print("3. Australia (+61)", style=STYLES['data'])
        console.print("4. Other (specify country code)", style=STYLES['data'])

        country_choice = prompt_choice("Select country", choices=["1", "2", "3", "4"], default="1")
        country_codes = get_country_codes()
        
        country_code = country_codes.get(country_choice)
        if country_choice == "4":
            country_code = prompt_choice("Enter country code (with +)", choices=None)

        # Search for numbers
        print_info("Searching...")
        available_numbers = search_available_numbers_by_country(country_code)
        
        if not available_numbers:
            print_error("No numbers available in the selected region.")
            prompt_choice("\nPress Enter to return", choices=[""], default="")
            return

        # Display available numbers
        print_panel("Available Numbers:", style='highlight')
        table = create_table(columns=["#", "Phone Number", "Region", "Monthly Cost"])
        for idx, number in enumerate(available_numbers, 1):
            table.add_row(
                str(idx),
                number['phoneNumber'],
                f"{number.get('region', 'N/A')}",
                f"${number.get('monthlyPrice', 'N/A')}",
                style=STYLES['data']
            )
        console.print(table)

        # Get user selection
        selection = prompt_choice(
            "\nSelect a number to purchase (0 to cancel)",
            choices=[str(i) for i in range(len(available_numbers) + 1)]
        )

        if selection == "0":
            print_warning("Purchase cancelled.")
            return

        # Purchase selected number
        selected_number = available_numbers[int(selection) - 1]['phoneNumber']
        if self._confirm_purchase(selected_number):
            self._execute_purchase(selected_number)

    def _confirm_purchase(self, phone_number):
        """Confirm purchase with the user.
        
        Args:
            phone_number (str): Phone number to purchase
            
        Returns:
            bool: True if confirmed, False if cancelled
        """
        if not confirm_action(f"Are you sure you want to purchase {phone_number}?"):
            print_warning("Purchase cancelled.")
            return False
        return True

    def _execute_purchase(self, phone_number):
        """Execute the purchase of a phone number.
        
        Args:
            phone_number (str): Phone number to purchase
        """
        success = purchase_phone_number(phone_number)

        if success:
            print_success(f"Number {phone_number} purchased successfully!")
        else:
            print_error(f"Failed to purchase number {phone_number}.")

        prompt_choice("\nPress Enter to return", choices=[""], default="")