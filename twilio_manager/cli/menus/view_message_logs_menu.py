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

class ViewMessageLogsMenu(BaseMenu):
    def show(self):
        """Display the view message logs menu."""
        options = {
            "1": "View message history",
            "0": "Return to previous menu"
        }
        self.display("Message Logs", "📝", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice == "1":
            from twilio_manager.cli.commands.view_logs_command import (
                get_message_logs,
                format_message_log_entry,
                display_message_logs
            )
            
            # Get and display logs
            logs = get_message_logs()
            if not logs:
                print_error("No message logs found.")
                prompt_choice("\nPress Enter to return", choices=[""], default="")
                return

            # Display logs with formatting
            display_message_logs(logs)