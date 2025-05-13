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
    def show(self):
        """Display the configure menu and handle configuration flow."""
        # Get active numbers
        active_numbers = get_active_numbers_list()
        if not active_numbers:
            print_warning("No active numbers found in your account.")
            prompt_choice("\nPress Enter to return", choices=[""], default="")
            return

        # Display active numbers
        print_panel("Select a number to configure:", style='highlight')
        table = create_table(columns=["#", "Phone Number", "Friendly Name", "Voice URL", "SMS URL"])
        for idx, number in enumerate(active_numbers, 1):
            table.add_row(
                str(idx),
                number['phoneNumber'],
                number.get('friendlyName', 'N/A'),
                number.get('voiceUrl', 'N/A'),
                number.get('smsUrl', 'N/A'),
                style=STYLES['data']
            )
        console.print(table)

        # Select number
        max_index = len(active_numbers)
        selection = prompt_choice(
            "\nSelect a number (0 to cancel)",
            choices=[str(i) for i in range(max_index + 1)]
        )

        if selection == "0":
            print_warning("Configuration cancelled.")
            return

        selected_number = active_numbers[int(selection) - 1]

        # Show current settings
        print_panel("Current Settings", style='highlight')
        print_info(f"Phone Number: {selected_number['phoneNumber']}")
        console.print("Friendly Name:", style=STYLES['dim'])
        console.print(selected_number.get('friendlyName', 'N/A'), style=STYLES['info'])
        console.print("\nVoice URL:", style=STYLES['dim'])
        console.print(selected_number.get('voiceUrl', 'N/A'), style=STYLES['info'])
        console.print("\nSMS URL:", style=STYLES['dim'])
        console.print(selected_number.get('smsUrl', 'N/A'), style=STYLES['info'])

        # Configuration options
        print_panel("\nWhat would you like to configure?", style='highlight')
        console.print("1. Friendly Name", style=STYLES['data'])
        console.print("2. Voice Webhook URL", style=STYLES['data'])
        console.print("3. SMS Webhook URL", style=STYLES['data'])
        console.print("4. All Settings", style=STYLES['data'])
        
        config_choice = prompt_choice("Select option", choices=["1", "2", "3", "4"])
        
        changes = {}
        
        if config_choice in ["1", "4"]:
            changes['friendly_name'] = prompt_choice(
                "Enter new friendly name",
                choices=None,
                default=selected_number.get('friendlyName', '')
            )
        
        if config_choice in ["2", "4"]:
            changes['voice_url'] = prompt_choice(
                "Enter new voice webhook URL",
                choices=None,
                default=selected_number.get('voiceUrl', '')
            )
        
        if config_choice in ["3", "4"]:
            changes['sms_url'] = prompt_choice(
                "Enter new SMS webhook URL",
                choices=None,
                default=selected_number.get('smsUrl', '')
            )

        # Show summary of changes
        print_panel("Review Changes", style='highlight')
        if changes.get('friendly_name'):
            console.print("Friendly Name:", style=STYLES['dim'])
            console.print(selected_number.get('friendlyName', 'N/A'), style=STYLES['error'])
            console.print("→", style=STYLES['dim'])
            console.print(changes['friendly_name'], style=STYLES['success'])
        if changes.get('voice_url'):
            console.print("\nVoice URL:", style=STYLES['dim'])
            console.print(selected_number.get('voiceUrl', 'N/A'), style=STYLES['error'])
            console.print("→", style=STYLES['dim'])
            console.print(changes['voice_url'], style=STYLES['success'])
        if changes.get('sms_url'):
            console.print("\nSMS URL:", style=STYLES['dim'])
            console.print(selected_number.get('smsUrl', 'N/A'), style=STYLES['error'])
            console.print("→", style=STYLES['dim'])
            console.print(changes['sms_url'], style=STYLES['success'])

        if not confirm_action("\nApply these changes?"):
            print_warning("Configuration cancelled.")
            return

        # Apply changes
        success = configure_phone_number(
            selected_number['sid'],
            friendly_name=changes.get('friendly_name'),
            voice_url=changes.get('voice_url'),
            sms_url=changes.get('sms_url')
        )

        if success:
            print_success("Number configured successfully!")
        else:
            print_error("Failed to update number settings.")

        prompt_choice("\nPress Enter to return", choices=[""], default="")