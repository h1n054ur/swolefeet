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
        # Get active numbers
        active_numbers = get_active_numbers_list()
        if not active_numbers:
            print_warning("No active numbers found in your account.")
            prompt_choice("\nPress Enter to return", choices=[""], default="")
            return

        # Display active numbers
        print_panel("Active Numbers:", style='highlight')
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
        selection = prompt_choice(
            "\nSelect a number to release (0 to cancel)",
            choices=[str(i) for i in range(max_index + 1)]
        )

        if selection == "0":
            print_warning("Release cancelled.")
            return

        # Get selected number
        selected_number = active_numbers[int(selection) - 1]

        # Confirm release
        if not confirm_action(
            f"Are you sure you want to release number {selected_number['phoneNumber']}? "
            "This action is irreversible.",
            style='error'
        ):
            print_warning("Release cancelled.")
            return

        # Execute release
        success = release_phone_number(selected_number['sid'])

        if success:
            print_success(f"Number {selected_number['phoneNumber']} released successfully.")
        else:
            print_error(f"Failed to release number {selected_number['phoneNumber']}.")

        prompt_choice("\nPress Enter to return", choices=[""], default="")