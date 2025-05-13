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

class ConfigureMenu(BaseMenu):
    def show(self):
        """Display the configure menu."""
        options = {
            "1": "Configure phone number settings",
            "0": "Return to previous menu"
        }
        self.display("Configure Phone Number", "⚙️", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice == "1":
            from twilio_manager.cli.commands.configure_command import (
                get_number_selection,
                show_current_settings,
                collect_configuration_changes,
                apply_configuration_changes
            )
            
            # Get number selection
            selected_number = get_number_selection()
            if not selected_number:
                return

            # Show current settings
            show_current_settings(selected_number)

            # Collect configuration changes
            changes = collect_configuration_changes(selected_number)
            if not changes:
                return

            # Apply changes
            apply_configuration_changes(selected_number['sid'], changes)