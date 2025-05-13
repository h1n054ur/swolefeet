from twilio_manager.core.phone_numbers import release_number, get_active_numbers
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
    clear_screen,
    print_header,
    STYLES
)
from twilio_manager.cli.menus.base_menu import BaseMenu

class ReleaseMenu(BaseMenu):
    def show(self):
        """Entry point to show the release menu."""
        clear_screen()
        print_header("Release Phone Number", "🗑️")
        self._handle_release_flow()

    def _handle_release_flow(self):
        """Handle the release of a phone number."""
        # Get list of active numbers
        active_numbers = get_active_numbers()
        
        if not active_numbers:
            print_warning("No active numbers found in your account.")
            prompt_choice("\nPress Enter to return", choices=[""], default="")
            return

        print_panel("Active Numbers:", style='highlight')
        self._display_active_numbers(active_numbers)

        # Let user select a number by index
        max_index = len(active_numbers)
        selection = prompt_choice(
            "\nSelect a number to release (0 to cancel)",
            choices=[str(i) for i in range(max_index + 1)]
        )

        if selection == "0":
            print_warning("Release cancelled.")
            return

        selected_number = active_numbers[int(selection) - 1]
        if not confirm_action(
            f"Are you sure you want to release number {selected_number['phoneNumber']}? "
            "This action is irreversible.",
            style='error'
        ):
            print_warning("Release cancelled.")
            return

        success = release_number(selected_number['sid'])

        if success:
            print_success(f"Number {selected_number['phoneNumber']} released successfully.")
        else:
            print_error(f"Failed to release number {selected_number['phoneNumber']}.")

        prompt_choice("\nPress Enter to return", choices=[""], default="")

    def _display_active_numbers(self, numbers):
        """Display a table of active phone numbers.
        
        Args:
            numbers (list): List of phone number dictionaries
        """
        table = create_table(columns=["#", "Phone Number", "Friendly Name", "SID"])
        for idx, number in enumerate(numbers, 1):
            table.add_row(
                str(idx),
                number['phoneNumber'],
                number.get('friendlyName', 'N/A'),
                number['sid'],
                style=STYLES['data']
            )
        console.print(table)