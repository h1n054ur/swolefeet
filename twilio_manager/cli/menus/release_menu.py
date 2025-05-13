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

class ReleaseMenu(BaseMenu):
    def show(self):
        """Display the release menu."""
        options = {
            "1": "Release a phone number",
            "0": "Return to previous menu"
        }
        self.display("Release Phone Number", "🗑️", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice == "1":
            from twilio_manager.cli.commands.release_command import (
                get_number_to_release,
                confirm_release_action,
                execute_number_release
            )
            
            # Get number selection
            selected_number = get_number_to_release()
            if not selected_number:
                return

            # Confirm release
            if not confirm_release_action(selected_number):
                return

            # Execute release
            execute_number_release(selected_number)