from rich.progress import Progress
from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.cli.menus.search.search_parameters_menu import SearchParametersMenu
from twilio_manager.cli.menus.search.search_results_menu import SearchResultsMenu
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
from twilio_manager.core.phone_numbers import search_available_numbers

class SearchMenu(BaseMenu):
    def show(self):
        """Display search menu and handle the search flow."""
        # Get search parameters
        params = SearchParametersMenu().show()
        if not params:
            return

        # Show search criteria
        print_info("Searching...")
        print_panel("Search criteria:", style='highlight')
        console.print("Country:", style=STYLES['dim'])
        console.print(params['country_code'], style=STYLES['info'])
        console.print("\nType:", style=STYLES['dim'])
        console.print(params['number_type'], style=STYLES['info'])
        console.print("\nCapabilities:", style=STYLES['dim'])
        console.print(', '.join(params['capabilities']), style=STYLES['info'])
        if params['pattern']:
            console.print("\nPattern:", style=STYLES['dim'])
            console.print(params['pattern'], style=STYLES['info'])

        # Initialize progress bar
        with Progress() as progress:
            search_task = progress.add_task(
                description="[cyan]🔍 Searching for numbers...",
                total=500
            )
            
            def update_progress(count):
                progress.update(
                    search_task,
                    completed=min(count, 500),
                    description=f"[cyan]Found {count} numbers"
                )
            
            # Search for numbers with progress tracking
            results, status = search_available_numbers(
                params['country_code'],
                params['number_type'],
                params['capabilities'],
                params['pattern'],
                progress_callback=update_progress
            )

        # Show search status
        if status.startswith("Error"):
            print_error(f"Search error: {status}")
            prompt_choice("\nPress Enter to return", choices=[""], default="")
            return

        if not results:
            print_panel("No matching numbers found.", style='error')
            print_info("\nPossible reasons:")
            console.print("• No numbers available in the selected region", style=STYLES['data'])
            console.print("• No numbers match the selected capabilities", style=STYLES['data'])
            console.print("• Pattern too restrictive", style=STYLES['data'])
            console.print("• Service not available in the selected region", style=STYLES['data'])
            
            print_info("\nTry:")
            console.print("• Different region", style=STYLES['data'])
            console.print("• Fewer capabilities", style=STYLES['data'])
            console.print("• Remove pattern", style=STYLES['data'])
            
            prompt_choice("\nPress Enter to return", choices=[""], default="")
            return

        print_success(status)
        SearchResultsMenu(results, status).show()