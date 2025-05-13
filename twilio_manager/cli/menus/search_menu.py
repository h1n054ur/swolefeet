from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.commands.search_command import (
    collect_search_parameters,
    run_number_search,
    display_search_results
)

class SearchMenu(BaseMenu):
    def show(self):
        """Display the search menu and handle the search flow."""
        # Get search parameters
        params = collect_search_parameters()
        if not params:
            return

        # Execute search
        results, status = run_number_search(params)
        if not results:
            return

        # Display results with pagination
        display_search_results(results, status)