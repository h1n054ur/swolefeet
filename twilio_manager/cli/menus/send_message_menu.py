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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_numbers = None
        self.recent_contacts = None
        self.from_number = None
        self.to_number = None
        self.message_body = None
        self.state = 'sender'  # sender, recipient_type, recipient, message, confirm

    def show(self):
        """Display the send message menu and handle message sending flow."""
        self.active_numbers = get_active_numbers_list()
        if not self.active_numbers:
            self.print_warning("No active numbers found in your account.")
            self.pause_and_return()
            return

        self._show_sender_menu()

    def _show_sender_menu(self):
        """Show menu to select sender number."""
        options = {}
        for idx, number in enumerate(self.active_numbers, 1):
            options[str(idx)] = f"{number['phoneNumber']} ({number.get('friendlyName', 'N/A')})"
        
        self.state = 'sender'
        self.display(
            title="Select Sender Number",
            emoji="📱",
            options=options
        )

    def _show_recipient_type_menu(self):
        """Show menu to select recipient type."""
        self.recent_contacts = get_recent_contacts_list()
        options = {
            "1": "Choose from recent contacts" if self.recent_contacts else "Enter new number",
            "2": "Enter new number" if self.recent_contacts else None
        }
        options = {k: v for k, v in options.items() if v is not None}
        
        self.state = 'recipient_type'
        self.display(
            title="Select Recipient Type",
            emoji="👥",
            options=options
        )

    def _show_recent_contacts_menu(self):
        """Show menu to select from recent contacts."""
        options = {}
        for idx, contact in enumerate(self.recent_contacts, 1):
            options[str(idx)] = f"{contact['phoneNumber']} (Last: {contact.get('lastContact', 'N/A')})"
        
        self.state = 'recipient'
        self.display(
            title="Select Recent Contact",
            emoji="📞",
            options=options
        )

    def _show_confirmation_menu(self):
        """Show message confirmation menu."""
        # Display message summary first
        print_panel("Message Summary:", style='highlight')
        console.print("From:", style=STYLES['dim'])
        console.print(self.from_number, style=STYLES['info'])
        console.print("\nTo:", style=STYLES['dim'])
        console.print(self.to_number, style=STYLES['info'])
        console.print("\nMessage:", style=STYLES['dim'])
        console.print(self.message_body, style=STYLES['info'])

        options = {
            "1": "Send message",
            "2": "Cancel"
        }
        
        self.state = 'confirm'
        self.display(
            title="Confirm Message",
            emoji="✉️",
            options=options
        )

    def handle_choice(self, choice):
        """Handle menu selection based on current state."""
        if self.state == 'sender':
            self._handle_sender_choice(choice)
        elif self.state == 'recipient_type':
            self._handle_recipient_type_choice(choice)
        elif self.state == 'recipient':
            self._handle_recipient_choice(choice)
        elif self.state == 'message':
            self._handle_message_input()
        elif self.state == 'confirm':
            self._handle_confirmation_choice(choice)

    def _handle_sender_choice(self, choice):
        """Handle sender number selection."""
        try:
            idx = int(choice) - 1
            self.from_number = self.active_numbers[idx]['phoneNumber']
            self.print_success(f"Selected sender: {self.from_number}")
            self._show_recipient_type_menu()
        except (ValueError, IndexError):
            self.print_error("Invalid selection")
            self.pause_and_return()

    def _handle_recipient_type_choice(self, choice):
        """Handle recipient type selection."""
        if choice == "1" and self.recent_contacts:
            self._show_recent_contacts_menu()
        else:
            self.state = 'message'
            self._handle_manual_recipient_input()

    def _handle_recipient_choice(self, choice):
        """Handle recipient selection from recent contacts."""
        try:
            idx = int(choice) - 1
            self.to_number = self.recent_contacts[idx]['phoneNumber']
            self.print_success(f"Selected recipient: {self.to_number}")
            self.state = 'message'
            self._handle_message_input()
        except (ValueError, IndexError):
            self.print_error("Invalid selection")
            self.pause_and_return()

    def _handle_manual_recipient_input(self):
        """Handle manual recipient number input."""
        to_number = prompt_choice("Enter recipient's number (E.164 format, e.g., +14155559876)", choices=None)
        if not validate_recipient_number(to_number):
            self.print_error("Invalid recipient number format.")
            self.pause_and_return()
            return
        
        self.to_number = to_number
        self.print_success(f"Recipient number: {self.to_number}")
        self._handle_message_input()

    def _handle_message_input(self):
        """Handle message body input."""
        self.message_body = prompt_choice("\nMessage body", choices=None)
        if not self.message_body:
            self.print_warning("Empty message not allowed.")
            self.pause_and_return()
            return
        
        self._show_confirmation_menu()

    def _handle_confirmation_choice(self, choice):
        """Handle send confirmation."""
        if choice == "1":
            params = prepare_message_params(self.from_number, self.to_number, self.message_body)
            success = send_sms_message(params)

            if success:
                self.print_success(f"Message sent successfully to {self.to_number}!")
            else:
                self.print_error(f"Failed to send message to {self.to_number}.")
        else:
            self.print_warning("Message cancelled.")
            
        self.pause_and_return()