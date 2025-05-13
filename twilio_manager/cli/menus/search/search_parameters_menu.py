from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    print_panel,
    prompt_choice,
    STYLES
)

class SearchParametersMenu(BaseMenu):
    def __init__(self, parent=None):
        """Initialize search parameters menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu to return to
        """
        super().__init__(parent)

    def show(self):
        """Collect search parameters from user input."""
        self.clear()
        self.print_title("Search Parameters", "🔍")

        # Country selection
        self.print_info("Select country:")
        self.print_option("1", "US/Canada (+1)")
        self.print_option("2", "UK (+44)")
        self.print_option("3", "Australia (+61)")
        self.print_option("4", "Other (specify country code)")
        
        from twilio_manager.shared.utils.logger import get_logger
        logger = get_logger(__name__)
        
        country_choice = self.get_choice(["1", "2", "3", "4"], "Select country", "1")
        country_codes = {
            "1": "US",  # US/Canada
            "2": "GB",  # UK
            "3": "AU"   # Australia
        }
        
        country_code = country_codes.get(country_choice)
        if country_choice == "4":
            # For custom country code, accept with or without +
            custom_code = self.get_choice(None, "Enter country code (e.g., US, GB)")
            country_code = custom_code.strip().lstrip('+').upper()
            
        logger.debug(f"Selected country code: {country_code}")

        # Number type selection
        self.clear()
        self.print_title("Number Type", "📱")
        self.print_info("Select number type:")
        self.print_option("1", "Local")
        self.print_option("2", "Mobile")
        self.print_option("3", "Toll-Free")
        
        type_choice = self.get_choice(["1", "2", "3"], "Select type", "1")
        number_types = {
            "1": "local",
            "2": "mobile",
            "3": "tollfree"
        }
        number_type = number_types[type_choice]

        # Capabilities selection
        self.clear()
        self.print_title("Capabilities", "⚡")
        self.print_info("Select capabilities:")
        self.print_option("1", "Voice + SMS")
        self.print_option("2", "Voice only")
        self.print_option("3", "SMS only")
        self.print_option("4", "All (Voice + SMS + MMS)")
        
        caps_choice = self.get_choice(["1", "2", "3", "4"], "Select capabilities", "1")
        capabilities_map = {
            "1": ["VOICE", "SMS"],
            "2": ["VOICE"],
            "3": ["SMS"],
            "4": ["VOICE", "SMS", "MMS"]
        }
        capabilities = capabilities_map[caps_choice]

        # Optional pattern
        self.clear()
        self.print_title("Number Pattern", "🔢")
        self.print_info("Number pattern (optional):")
        self.print_option("1", "No pattern")
        self.print_option("2", "Enter custom pattern")
        
        pattern_choice = self.get_choice(["1", "2"], "Select option", "1")
        pattern = "" if pattern_choice == "1" else self.get_choice(None, "Enter pattern (e.g., 555)")

        return {
            'country_code': country_code,
            'number_type': number_type,
            'capabilities': capabilities,
            'pattern': pattern
        }