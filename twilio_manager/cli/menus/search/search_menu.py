from rich.progress import Progress, SpinnerColumn, TextColumn
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
from twilio_manager.shared.utils.logger import get_logger

logger = get_logger(__name__)

class SearchMenu(BaseMenu):
    def __init__(self, parent=None):
        """Initialize search menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu to return to
        """
        super().__init__(parent)

    def show(self):
        """Display search menu and handle the search flow."""
        try:
            # Get search parameters
            params = SearchParametersMenu(parent=self).show()
            if not params:
                self.return_to_parent()
                return

            # Show search criteria
            self.clear()
            self.print_title("Search Criteria", "🔍")
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

            # Initialize progress bar with better visibility
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=False  # Keep progress visible
            ) as progress:
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
                
                try:
                    # Search for numbers with progress tracking
                    results, status = search_available_numbers(
                        params['country_code'],
                        params['number_type'],
                        params['capabilities'],
                        params['pattern'],
                        progress_callback=update_progress
                    )
                except Exception as e:
                    logger.error(f"Search failed: {str(e)}", exc_info=True)
                    self.print_error(f"Search failed: {str(e)}")
                    self.pause_and_return()
                    return

            # Show search status
            if status.startswith("Error"):
                logger.error(f"Search error: {status}")
                self.print_error(f"Search error: {status}")
                self.pause_and_return()
                return

            if not results:
                self.clear()
                self.print_title("No Results", "❌")
                print_panel("No matching numbers found.", style='error')
                self.print_info("\nPossible reasons:")
                console.print("• No numbers available in the selected region", style=STYLES['data'])
                console.print("• No numbers match the selected capabilities", style=STYLES['data'])
                console.print("• Pattern too restrictive", style=STYLES['data'])
                console.print("• Service not available in the selected region", style=STYLES['data'])
                
                self.print_info("\nTry:")
                console.print("• Different region", style=STYLES['data'])
                console.print("• Fewer capabilities", style=STYLES['data'])
                console.print("• Remove pattern", style=STYLES['data'])
                
                self.pause_and_return()
                return

            self.print_success(status)
            SearchResultsMenu(results, status, parent=self).show()
            
        except Exception as e:
            logger.error(f"Unexpected error in search menu: {str(e)}", exc_info=True)
            self.print_error(f"An unexpected error occurred: {str(e)}")
            self.pause_and_return()