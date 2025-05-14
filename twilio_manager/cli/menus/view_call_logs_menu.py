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
    STYLES
)
from twilio_manager.cli.commands.view_logs_command import (
    get_call_logs_list,
    format_call_log_entry
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
            # Get logs
            logs = get_call_logs_list()
            if not logs:
                print_error("No call logs found.")
                prompt_choice("\nPress Enter to return", choices=[""], default="")
                return

            # Format and display logs
            print_panel("Call History", style='highlight')
            table = create_table(columns=["From", "To", "Status", "Duration", "Start Time"])
            
            for log in logs:
                formatted = format_call_log_entry(log)
                table.add_row(
                    formatted['from'],
                    formatted['to'],
                    formatted['status'],
                    formatted['duration'] + " sec",
                    formatted['start_time'],
                    style=STYLES['data']
                )
            
            console.print(table)
            prompt_choice("\nPress Enter to return", choices=[""], default="")