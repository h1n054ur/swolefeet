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
from twilio_manager.cli.commands.release_command import (
    get_active_numbers_list,
    release_phone_number
)

class ReleaseMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_numbers = None
        self.selected_number = None
        self.state = 'select'  # select, confirm

    def show(self):
        """Display the release menu and handle release flow."""
        self.active_numbers = get_active_numbers_list()
        if not self.active_numbers:
            self.print_warning("No active numbers found in your account.")
            self.pause_and_return()
            return

        self._show_selection_menu()

    def _show_selection_menu(self):
        """Show menu to select a number to release."""
        self._display_active_numbers()
        options = {}
        for idx, number in enumerate(self.active_numbers, 1):
            options[str(idx)] = f"{number['phoneNumber']} ({number.get('friendlyName', 'N/A')})"
        
        self.state = 'select'
        self.display(
            title="Release Phone Number",
            emoji="🗑️",
            options=options
        )

    def _show_confirmation_menu(self):
        """Show release confirmation menu."""
        self._display_active_numbers()
        options = {
            "1": f"Yes, release {self.selected_number['phoneNumber']}",
            "2": "No, cancel release"
        }
        
        self.state = 'confirm'
        self.display(
            title="Confirm Release",
            emoji="⚠️",
            options=options
        )

    def _display_active_numbers(self):
        """Display active numbers in a table."""
        table = create_table(columns=["#", "Phone Number", "Friendly Name", "SID"])
        for idx, number in enumerate(self.active_numbers, 1):
            table.add_row(
                str(idx),
                number['phoneNumber'],
                number.get('friendlyName', 'N/A'),
                number['sid'],
                style=STYLES['data']
            )
        console.print(table)

    def handle_choice(self, choice):
        """Handle menu selection based on current state."""
        if self.state == 'select':
            self._handle_selection_choice(choice)
        elif self.state == 'confirm':
            self._handle_confirmation_choice(choice)

    def _handle_selection_choice(self, choice):
        """Handle number selection."""
        try:
            idx = int(choice) - 1
            self.selected_number = self.active_numbers[idx]
            self.print_info(
                f"\nSelected number: {self.selected_number['phoneNumber']}\n"
                "⚠️ WARNING: This action is irreversible!"
            )
            self._show_confirmation_menu()
        except (ValueError, IndexError):
            self.print_error("Invalid selection")
            self.pause_and_return()

    def _handle_confirmation_choice(self, choice):
        """Handle release confirmation."""
        if choice == "1":
            success = release_phone_number(self.selected_number['sid'])
            if success:
                self.print_success(f"Number {self.selected_number['phoneNumber']} released successfully.")
            else:
                self.print_error(f"Failed to release number {self.selected_number['phoneNumber']}.")
        else:
            self.print_warning("Release cancelled.")
        
        self.pause_and_return()