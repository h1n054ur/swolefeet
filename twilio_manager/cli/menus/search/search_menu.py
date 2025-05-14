# File: twilio_manager/cli/menus/search/search_menu.py

from typing import List, Dict, Optional, Callable
from rich.progress import Progress
from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.menus.search.search_parameters_menu import SearchParametersMenu
from twilio_manager.cli.menus.search.search_results_menu import SearchResultsMenu
from twilio_manager.shared.ui.styling import (
    console,
    print_success,
    print_error,
    print_info,
    STYLES
)
from twilio_manager.core.phone_numbers import search_available_numbers

class SearchMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

    def show(self):
        """Display search menu and handle the search flow."""
        # 1) Collect parameters
        params = SearchParametersMenu(parent=self).show()
        if not params:
            self.return_to_parent()
            return

        # 2) Display the criteria back to the user
        self.clear()
        self.print_title("Search Criteria", "🔍")
        console.print("Country:", style=STYLES["dim"])
        console.print(params["country_code"], style=STYLES["info"])
        console.print("\nType:", style=STYLES["dim"])
        console.print(params["number_type"], style=STYLES["info"])
        console.print("\nCapabilities:", style=STYLES["dim"])
        console.print(", ".join(params["capabilities"]), style=STYLES["info"])
        if params.get("pattern"):
            console.print("\nPattern:", style=STYLES["dim"])
            console.print(params["pattern"], style=STYLES["info"])

        # ← Add a blank line here for spacing
        console.print("")

        # 3) Run the search with a live progress bar (up to 500)
        with Progress() as progress:
            task_id = progress.add_task(
                "[cyan]🔍 Searching for numbers...", total=500
            )

            def update_progress(count: int):
                progress.update(
                    task_id,
                    completed=min(count, 500),
                    description=f"[cyan]Found {count} numbers"
                )

            try:
                results, status = search_available_numbers(
                    params["country_code"],
                    params["number_type"],
                    params["capabilities"],
                    params.get("pattern", ""),
                    progress_callback=update_progress
                )
            except Exception as e:
                self.clear()
                self.print_error(f"Search error: {e}")
                self.get_choice([""], "\nPress Enter to return", "")
                return

        # 4) Handle error status
        if isinstance(status, str) and status.startswith("Error"):
            self.clear()
            self.print_error(f"Search error: {status}")
            self.print_info("\nDebug Information:")
            console.print(f"Country: {params['country_code']}", style=STYLES["data"])
            console.print(f"Type: {params['number_type']}", style=STYLES["data"])
            console.print(f"Capabilities: {', '.join(params['capabilities'])}", style=STYLES["data"])
            if params.get("pattern"):
                console.print(f"Pattern: {params['pattern']}", style=STYLES["data"])
            self.pause_and_return()
            return

        # 5) No results found
        if not results:
            self.clear()
            self.print_title("No Results", "❌")
            print_info("No matching numbers found.")
            self.print_info("\nPossible reasons:")
            console.print("• No numbers available in the selected region", style=STYLES["data"])
            console.print("• No numbers match the selected capabilities", style=STYLES["data"])
            console.print("• Pattern too restrictive", style=STYLES["data"])
            console.print("• Service not available in the selected region", style=STYLES["data"])
            self.print_info("\nTry:")
            console.print("• Different region", style=STYLES["data"])
            console.print("• Fewer capabilities", style=STYLES["data"])
            console.print("• Remove pattern", style=STYLES["data"])
            self.pause_and_return()
            return

        # 6) Success — show results
        self.clear()
        self.print_title("Search Results", "📱")
        self.print_success(status)
        SearchResultsMenu(results, status, parent=self).show()
        self.return_to_parent()
