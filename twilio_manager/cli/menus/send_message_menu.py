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
from twilio_manager.cli.commands.send_message_command import (
    get_active_numbers_list,
    get_recent_contacts_list,
    validate_recipient_number,
    prepare_message_params,
    send_sms_message
)

class SendMessageMenu(BaseMenu):
    def show(self):
        """Display the send message menu and handle message sending flow."""
        self.clear()
        self.print_title("Send Message", "✉️")

        # Get active numbers
        active_numbers = get_active_numbers_list()
        if not active_numbers:
            self.print_warning("No active numbers found in your account.")
            self.get_choice([""], "\nPress Enter to return", "")
            return

        # Display active numbers
        self.print_panel("Select a number to send from:", style='highlight')
        table = create_table(columns=["#", "Phone Number", "Friendly Name"])
        for idx, number in enumerate(active_numbers, 1):
            table.add_row(
                str(idx),
                number['phoneNumber'],
                number.get('friendlyName', 'N/A'),
                style=STYLES['data']
            )
        console.print(table)

        # Select sender number
        max_index = len(active_numbers)
        selection = self.get_choice(
            [str(i) for i in range(max_index + 1)],
            "\nSelect a number (0 to cancel)"
        )

        if selection == "0":
            self.print_warning("Message cancelled.")
            return

        from_number = active_numbers[int(selection) - 1]['phoneNumber']

        # Get recent contacts
        recent_contacts = get_recent_contacts_list()
        
        # Select recipient
        self.print_panel("Select recipient:", style='highlight')
        console.print("1. Choose from recent contacts", style=STYLES['data'])
        console.print("2. Enter new number", style=STYLES['data'])
        
        recipient_choice = self.get_choice(["1", "2"], "Select option")
        
        if recipient_choice == "1" and recent_contacts:
            self.print_panel("Recent Contacts:", style='highlight')
            table = create_table(columns=["#", "Phone Number", "Last Contact"])
            for idx, contact in enumerate(recent_contacts, 1):
                table.add_row(
                    str(idx),
                    contact['phoneNumber'],
                    contact.get('lastContact', 'N/A'),
                    style=STYLES['data']
                )
            console.print(table)
            
            max_contact_index = len(recent_contacts)
            contact_selection = self.get_choice(
                [str(i) for i in range(max_contact_index + 1)],
                "\nSelect a contact (0 to enter new number)"
            )
            
            if contact_selection == "0":
                to_number = self.get_choice(None, "Enter recipient's number (E.164 format, e.g., +14155559876)")
            else:
                to_number = recent_contacts[int(contact_selection) - 1]['phoneNumber']
        else:
            to_number = self.get_choice(None, "Enter recipient's number (E.164 format, e.g., +14155559876)")

        # Validate recipient number
        if not validate_recipient_number(to_number):
            self.print_error("Invalid recipient number format.")
            self.get_choice([""], "\nPress Enter to return", "")
            return

        # Get message body
        body = self.get_choice(None, "\nMessage body")

        # Show summary and confirm
        self.print_panel("Message Summary:", style='highlight')
        console.print("From:", style=STYLES['dim'])
        console.print(from_number, style=STYLES['info'])
        console.print("\nTo:", style=STYLES['dim'])
        console.print(to_number, style=STYLES['info'])
        console.print("\nMessage:", style=STYLES['dim'])
        console.print(body, style=STYLES['info'])

        if not confirm_action("Send this message?"):
            self.print_warning("Message not sent.")
            self.get_choice([""], "\nPress Enter to return", "")
            return

        # Send message
        params = prepare_message_params(from_number, to_number, body)
        success = send_sms_message(params)

        if success:
            self.print_success(f"Message sent successfully to {to_number}!")
        else:
            self.print_error(f"Failed to send message to {to_number}.")

        self.get_choice([""], "\nPress Enter to return", "")