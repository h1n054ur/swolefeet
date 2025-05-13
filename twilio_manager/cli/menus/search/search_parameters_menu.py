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
from twilio_manager.shared.utils.logger import get_logger

logger = get_logger(__name__)

class SearchParametersMenu(BaseMenu):
    def __init__(self, parent=None):
        """Initialize search parameters menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu to return to
        """
        super().__init__(parent)

    def show(self):
        """Display search parameters menu and get user input.
        
        Returns:
            dict: Search parameters or None if cancelled
        """
        try:
            self.clear()
            self.print_title("Search Parameters", "🔍")
            
            # Get country code
            print_panel("Select country code:", style='info')
            self.print_option("1", "United States (+1)")
            self.print_option("2", "United Kingdom (+44)")
            self.print_option("3", "Australia (+61)")
            self.print_option("0", "Cancel")
            
            choice = self.get_choice(["0", "1", "2", "3"], "Select country")
            if choice == "0":
                return None
                
            country_map = {
                "1": "+1",
                "2": "+44",
                "3": "+61"
            }
            country_code = country_map[choice]
            
            # Get number type
            self.clear()
            self.print_title("Number Type", "📱")
            print_panel("Select number type:", style='info')
            self.print_option("1", "Local")
            self.print_option("2", "Toll-Free")
            self.print_option("3", "Mobile")
            self.print_option("0", "Cancel")
            
            choice = self.get_choice(["0", "1", "2", "3"], "Select type")
            if choice == "0":
                return None
                
            type_map = {
                "1": "local",
                "2": "tollfree",
                "3": "mobile"
            }
            number_type = type_map[choice]
            
            # Get capabilities
            self.clear()
            self.print_title("Capabilities", "⚡")
            print_panel("Select capabilities (space-separated numbers):", style='info')
            self.print_option("1", "Voice")
            self.print_option("2", "SMS")
            self.print_option("3", "MMS")
            self.print_option("0", "Cancel")
            
            choice = self.get_choice(["0", "1", "2", "3", "12", "13", "23", "123"], "Select capabilities")
            if choice == "0":
                return None
                
            capabilities = []
            if "1" in choice:
                capabilities.append("VOICE")
            if "2" in choice:
                capabilities.append("SMS")
            if "3" in choice:
                capabilities.append("MMS")
            
            # Get pattern (optional)
            self.clear()
            self.print_title("Pattern", "🔤")
            print_panel("Enter search pattern (optional):", style='info')
            self.print_info("• For US numbers, enter area code (e.g., 415)")
            self.print_info("• For other regions, enter any part of the number")
            self.print_info("• Leave empty for no pattern")
            
            pattern = input("Pattern (or press Enter to skip): ").strip()
            
            return {
                "country_code": country_code,
                "number_type": number_type,
                "capabilities": capabilities,
                "pattern": pattern
            }
            
        except Exception as e:
            logger.error(f"Error in search parameters menu: {str(e)}", exc_info=True)
            self.print_error("An error occurred. Please try again.")
            self.pause_and_return()
            return None