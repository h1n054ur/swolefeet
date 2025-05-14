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

    def __init__(self, parent=None):
        """Initialize search parameters menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu to return to
        """
        super().__init__(parent)
        self.state = 'country'  # country, type, capabilities, pattern
        self.params = {
            'country_code': None,
            'number_type': None,
            'capabilities': None,
            'pattern': None
        }
        self.logger = get_logger(__name__)

    def show(self):
        """Collect search parameters from user input."""
        self.state = 'country'
        self._show_country_menu()
        return self.params

    def _show_country_menu(self):
        """Show country selection menu."""
        options = {
            "1": "US/Canada (+1)",
            "2": "UK (+44)",
            "3": "Australia (+61)",
            "4": "Other (specify country code)"
        }
        self.display(
            title="Search Parameters - Country",
            emoji="🔍",
            options=options
        )

    def _show_type_menu(self):
        """Show number type selection menu."""
        options = {
            "1": "Local",
            "2": "Mobile",
            "3": "Toll-Free"
        }
        self.display(
            title="Search Parameters - Number Type",
            emoji="📱",
            options=options
        )

    def _show_capabilities_menu(self):
        """Show capabilities selection menu."""
        options = {
            "1": "Voice + SMS",
            "2": "Voice only",
            "3": "SMS only",
            "4": "All (Voice + SMS + MMS)"
        }
        self.display(
            title="Search Parameters - Capabilities",
            emoji="⚡",
            options=options
        )

    def _show_pattern_menu(self):
        """Show pattern selection menu."""
        options = {
            "1": "No pattern",
            "2": "Enter custom pattern"
        }
        self.display(
            title="Search Parameters - Number Pattern",
            emoji="🔢",
            options=options
        )

    def handle_choice(self, choice):
        """Handle menu selection based on current state."""
        if self.state == 'country':
            self._handle_country_choice(choice)
        elif self.state == 'type':
            self._handle_type_choice(choice)
        elif self.state == 'capabilities':
            self._handle_capabilities_choice(choice)
        elif self.state == 'pattern':
            self._handle_pattern_choice(choice)

    def _handle_country_choice(self, choice):
        """Handle country selection."""
        country_codes = {
            "1": "US",  # US/Canada
            "2": "GB",  # UK
            "3": "AU"   # Australia
        }
        
        if choice == "4":
            custom_code = self.get_choice(None, "Enter country code (e.g., US, GB)")
            self.params['country_code'] = custom_code.strip().lstrip('+').upper()
        else:
            self.params['country_code'] = country_codes[choice]
        
        self.logger.debug(f"Selected country code: {self.params['country_code']}")
        self.state = 'type'
        self._show_type_menu()

    def _handle_type_choice(self, choice):
        """Handle number type selection."""
        number_types = {
            "1": "local",
            "2": "mobile",
            "3": "tollfree"
        }
        self.params['number_type'] = number_types[choice]
        self.state = 'capabilities'
        self._show_capabilities_menu()

    def _handle_capabilities_choice(self, choice):
        """Handle capabilities selection."""
        capabilities_map = {
            "1": ["VOICE", "SMS"],
            "2": ["VOICE"],
            "3": ["SMS"],
            "4": ["VOICE", "SMS", "MMS"]
        }
        self.params['capabilities'] = capabilities_map[choice]
        self.state = 'pattern'
        self._show_pattern_menu()

    def _handle_pattern_choice(self, choice):
        """Handle pattern selection."""
        if choice == "1":
            self.params['pattern'] = ""
        else:
            pattern = self.get_choice(None, "Enter pattern (e.g., 555)")
            self.params['pattern'] = pattern

        self.print_success("Search parameters configured successfully!")
        self.pause_and_return()