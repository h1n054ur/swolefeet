from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    print_panel,
    prompt_choice,
    STYLES
)

class SearchParametersMenu(BaseMenu):
    def show(self):
        """Collect search parameters from user input."""
        # Country selection
        print_panel("Select country:", style='highlight')
        console.print("1. US/Canada (+1)", style=STYLES['data'])
        console.print("2. UK (+44)", style=STYLES['data'])
        console.print("3. Australia (+61)", style=STYLES['data'])
        console.print("4. Other (specify country code)", style=STYLES['data'])
        
        country_choice = prompt_choice("Select country", choices=["1", "2", "3", "4"], default="1")
        country_codes = {
            "1": "+1",
            "2": "+44",
            "3": "+61"
        }
        
        country_code = country_codes.get(country_choice)
        if country_choice == "4":
            country_code = prompt_choice("Enter country code (with +)", choices=None)

        # Number type selection
        print_panel("Select number type:", style='highlight')
        console.print("1. Local", style=STYLES['data'])
        console.print("2. Mobile", style=STYLES['data'])
        console.print("3. Toll-Free", style=STYLES['data'])
        
        type_choice = prompt_choice("Select type", choices=["1", "2", "3"], default="1")
        number_types = {
            "1": "local",
            "2": "mobile",
            "3": "tollfree"
        }
        number_type = number_types[type_choice]

        # Capabilities selection
        print_panel("Select capabilities:", style='highlight')
        console.print("1. Voice + SMS", style=STYLES['data'])
        console.print("2. Voice only", style=STYLES['data'])
        console.print("3. SMS only", style=STYLES['data'])
        console.print("4. All (Voice + SMS + MMS)", style=STYLES['data'])
        
        caps_choice = prompt_choice("Select capabilities", choices=["1", "2", "3", "4"], default="1")
        capabilities_map = {
            "1": ["VOICE", "SMS"],
            "2": ["VOICE"],
            "3": ["SMS"],
            "4": ["VOICE", "SMS", "MMS"]
        }
        capabilities = capabilities_map[caps_choice]

        # Optional pattern
        print_panel("Number pattern (optional):", style='highlight')
        console.print("1. No pattern", style=STYLES['data'])
        console.print("2. Enter custom pattern", style=STYLES['data'])
        
        pattern_choice = prompt_choice("Select option", choices=["1", "2"], default="1")
        pattern = "" if pattern_choice == "1" else prompt_choice("Enter pattern (e.g., 555)", choices=None)

        return {
            'country_code': country_code,
            'number_type': number_type,
            'capabilities': capabilities,
            'pattern': pattern
        }