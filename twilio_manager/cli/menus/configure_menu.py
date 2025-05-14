from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_panel,
    print_success,
    print_error,
    print_warning,
    print_info,
    prompt_choice,
    confirm_action,
    STYLES
)
from twilio_manager.cli.commands.configure_command import (
    get_active_numbers_list,
    configure_phone_number
)

class ConfigureMenu(BaseMenu):
    def __init__(self, parent=None):
        """Initialize the configure menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu
        """
        super().__init__(parent)
        self.active_numbers = []
        self.selected_number = None
        self.changes = {}

    def show(self):
        """Display the configure menu."""
        # Get active numbers
        self.active_numbers = get_active_numbers_list()
        if not self.active_numbers:
            self.print_warning("No active numbers found in your account.")
            self.pause_and_return()
            return

        # Create options dictionary
        options = {}
        for idx, number in enumerate(self.active_numbers, 1):
            friendly_name = number.get('friendlyName', 'N/A')
            options[str(idx)] = f"{number['phoneNumber']} ({friendly_name})"
        options["0"] = "Back"

        self.display("Select a number to configure", "⚙️", options)

    def handle_choice(self, choice):
        """Handle number selection and configuration.
        
        Args:
            choice (str): The user's selected option
        """
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(self.active_numbers):
            return

        self.selected_number = self.active_numbers[int(choice) - 1]
        self._show_current_settings()
        ConfigSettingsMenu(self, self.selected_number).show()

    def _show_current_settings(self):
        """Display current settings for selected number."""
        print_panel("Current Settings", style='highlight')
        print_info(f"Phone Number: {self.selected_number['phoneNumber']}")
        console.print("Friendly Name:", style=STYLES['dim'])
        console.print(self.selected_number.get('friendlyName', 'N/A'), style=STYLES['info'])
        console.print("\nVoice URL:", style=STYLES['dim'])
        console.print(self.selected_number.get('voiceUrl', 'N/A'), style=STYLES['info'])
        console.print("\nSMS URL:", style=STYLES['dim'])
        console.print(self.selected_number.get('smsUrl', 'N/A'), style=STYLES['info'])

class ConfigSettingsMenu(BaseMenu):
    def __init__(self, parent=None, number=None):
        """Initialize the settings menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu
            number (dict): Selected phone number details
        """
        super().__init__(parent)
        self.number = number
        self.changes = {}

    def show(self):
        """Display configuration options menu."""
        self.display("Configure Settings", "⚙️", {
            "1": "Friendly Name",
            "2": "Voice Webhook URL",
            "3": "SMS Webhook URL",
            "4": "All Settings",
            "0": "Back"
        })

    def handle_choice(self, choice):
        """Handle settings configuration.
        
        Args:
            choice (str): The user's selected option
        """
        if choice not in ["1", "2", "3", "4"]:
            return

        # Get changes based on selection
        if choice in ["1", "4"]:
            self.changes['friendly_name'] = self.get_choice(
                None,
                "Enter new friendly name",
                default=self.number.get('friendlyName', '')
            )
        
        if choice in ["2", "4"]:
            self.changes['voice_url'] = self.get_choice(
                None,
                "Enter new voice webhook URL",
                default=self.number.get('voiceUrl', '')
            )
        
        if choice in ["3", "4"]:
            self.changes['sms_url'] = self.get_choice(
                None,
                "Enter new SMS webhook URL",
                default=self.number.get('smsUrl', '')
            )

        # Show changes summary
        self._show_changes_summary()

        # Confirm and apply changes
        if confirm_action("\nApply these changes?"):
            success = configure_phone_number(
                self.number['sid'],
                friendly_name=self.changes.get('friendly_name'),
                voice_url=self.changes.get('voice_url'),
                sms_url=self.changes.get('sms_url')
            )

            if success:
                self.print_success("Number configured successfully!")
            else:
                self.print_error("Failed to update number settings.")
        else:
            self.print_warning("Configuration cancelled.")

        self.pause_and_return()

    def _show_changes_summary(self):
        """Display summary of changes to be made."""
        print_panel("Review Changes", style='highlight')
        if self.changes.get('friendly_name'):
            console.print("Friendly Name:", style=STYLES['dim'])
            console.print(self.number.get('friendlyName', 'N/A'), style=STYLES['error'])
            console.print("→", style=STYLES['dim'])
            console.print(self.changes['friendly_name'], style=STYLES['success'])
        if self.changes.get('voice_url'):
            console.print("\nVoice URL:", style=STYLES['dim'])
            console.print(self.number.get('voiceUrl', 'N/A'), style=STYLES['error'])
            console.print("→", style=STYLES['dim'])
            console.print(self.changes['voice_url'], style=STYLES['success'])
        if self.changes.get('sms_url'):
            console.print("\nSMS URL:", style=STYLES['dim'])
            console.print(self.number.get('smsUrl', 'N/A'), style=STYLES['error'])
            console.print("→", style=STYLES['dim'])
            console.print(self.changes['sms_url'], style=STYLES['success'])