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
    def show(self):
        """Display menu to select a caller number."""
        # Get active numbers with voice capability
        active_numbers = [n for n in get_active_numbers() if n.get('capabilities', {}).get('voice', False)]
        
        if not active_numbers:
            print_warning("No voice-enabled numbers found in your account.")
            prompt_choice("\nPress Enter to return", choices=[""], default="")
            return None

        # Select sender number
        print_panel("Select a number to call from:", style='highlight')
        self._display_phone_numbers(active_numbers)

        max_index = len(active_numbers)
        selection = prompt_choice(
            "\nSelect a number (0 to cancel)",
            choices=[str(i) for i in range(max_index + 1)]
        )

        if selection == "0":
            print_warning("Call cancelled.")
            return None

        return active_numbers[int(selection) - 1]['phoneNumber']

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