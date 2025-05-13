from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    print_panel,
    print_success,
    print_error,
    print_info,
    prompt_choice,
    STYLES,
    create_table
)

class SearchMenu(BaseMenu):
    def show(self):
        """Display the search menu."""
        options = {
            "1": "Search for available numbers",
            "0": "Return to previous menu"
        }
        self.display("Search Phone Numbers", "🔍", options)

    def handle_choice(self, choice):
        """Handle the user's menu choice."""
        if choice == "1":
            from twilio_manager.cli.commands.search_command import (
                collect_search_parameters,
                run_number_search,
                display_search_results
            )
            
            # Get search parameters from user
            params = collect_search_parameters()
            if not params:
                return

            # Execute the search
            results, status = run_number_search(params)
            if not results:
                return

            # Display and handle results pagination
            display_search_results(results, status)