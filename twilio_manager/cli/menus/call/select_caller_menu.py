from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_panel,
    print_warning,
    prompt_choice,
    STYLES
)
from twilio_manager.core.phone_numbers import get_active_numbers

class SelectCallerMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_numbers = None
        self.selected_number = None

    def show(self):
        """Display menu to select a caller number."""
        # Get active numbers with voice capability
        self.active_numbers = [n for n in get_active_numbers() if n.get('capabilities', {}).get('voice', False)]
        
        if not self.active_numbers:
            self.print_warning("No voice-enabled numbers found in your account.")
            self.pause_and_return()
            return None

        options = {}
        for idx, number in enumerate(self.active_numbers, 1):
            options[str(idx)] = f"{number['phoneNumber']} ({number.get('friendlyName', 'N/A')})"

        self.display(
            title="Select Caller Number",
            emoji="📞",
            options=options
        )
        
        return self.selected_number

    def handle_choice(self, choice):
        """Handle the user's menu selection."""
        try:
            idx = int(choice) - 1
            self.selected_number = self.active_numbers[idx]['phoneNumber']
            self.print_success(f"Selected number: {self.selected_number}")
            self.pause_and_return()

    def _display_phone_numbers(self, numbers):
        """Display a table of available phone numbers."""
        table = create_table(columns=["#", "Phone Number", "Friendly Name", "Voice Enabled"])
        
        for idx, number in enumerate(numbers, 1):
            voice_enabled = "✓" if number.get('capabilities', {}).get('voice', False) else "✗"
            table.add_row(
                str(idx),
                number['phoneNumber'],
                number.get('friendlyName', 'N/A'),
                voice_enabled,
                style=STYLES['data']
            )
        
        console.print(table)