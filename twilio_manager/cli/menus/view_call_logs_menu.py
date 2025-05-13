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

class ViewCallLogsMenu(BaseMenu):
    def show(self):
        """Display the view call logs menu."""
        options = {
            "1": "View call history",
            "0": "Return to previous menu"
        }
        self.display("Call Logs", "📊", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice == "1":
            from twilio_manager.cli.commands.view_logs_command import (
                get_call_logs,
                format_call_log_entry,
                display_call_logs
            )
            
            # Get and display logs
            logs = get_call_logs()
            if not logs:
                print_error("No call logs found.")
                prompt_choice("\nPress Enter to return", choices=[""], default="")
                return

            # Display logs with formatting
            display_call_logs(logs)