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
    def show(self):
        """Display the release menu and handle release flow."""
        self.clear()
        self.print_title("Release Numbers", "📱")

        # Get active numbers
        active_numbers = get_active_numbers_list()
        if not active_numbers:
            self.print_warning("No active numbers found in your account.")
            self.get_choice([""], "\nPress Enter to return", "")
            return

        # Display active numbers
        self.print_panel("Active Numbers:", style='highlight')
        table = create_table(columns=["#", "Phone Number", "Friendly Name", "SID"])
        for idx, number in enumerate(active_numbers, 1):
            table.add_row(
                str(idx),
                number['phoneNumber'],
                number.get('friendlyName', 'N/A'),
                number['sid'],
                style=STYLES['data']
            )
        console.print(table)

        # Let user select a number
        max_index = len(active_numbers)
        selection = self.get_choice(
            [str(i) for i in range(max_index + 1)],
            "\nSelect a number to release (0 to cancel)"
        )

        if selection == "0":
            self.print_warning("Release cancelled.")
            return

        # Get selected number
        selected_number = active_numbers[int(selection) - 1]

        # Confirm release
        if not confirm_action(
            f"Are you sure you want to release number {selected_number['phoneNumber']}? "
            "This action is irreversible.",
            style='error'
        ):
            self.print_warning("Release cancelled.")
            return

        # Execute release
        success = release_phone_number(selected_number['sid'])

        if success:
            self.print_success(f"Number {selected_number['phoneNumber']} released successfully.")
        else:
            self.print_error(f"Failed to release number {selected_number['phoneNumber']}.")

        self.get_choice([""], "\nPress Enter to return", "")