from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.menus.search.search_parameters_menu import SearchParametersMenu
from twilio_manager.cli.menus.search.search_results_menu import SearchResultsMenu
from twilio_manager.services.phone_service import PhoneService
from twilio_manager.shared.ui.styling import print_error, print_info

class SearchMenu(BaseMenu):
    def show(self):
        """Display the search menu and handle the search flow."""
        self.clear()
        self.print_title("Search Phone Numbers", "🔍")

        # Get search parameters using SearchParametersMenu
        params_menu = SearchParametersMenu()
        params = params_menu.show()
        if not params:
            return

        # Execute search using PhoneService
        self.print_info("Searching for available numbers...")
        try:
            phone_service = PhoneService()
            results = phone_service.search_numbers(**params)
            if not results:
                self.print_error("No numbers found matching your criteria.")
                self.get_choice([""], "\nPress Enter to return", "")
                return
            status = "success"  # We could enhance this with more detailed status info
        except Exception as e:
            self.print_error(f"Error searching for numbers: {str(e)}")
            self.get_choice([""], "\nPress Enter to return", "")
            return

        # Display results with pagination using SearchResultsMenu
        results_menu = SearchResultsMenu(results, status)
        results_menu.show()