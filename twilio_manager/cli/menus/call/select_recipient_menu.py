from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_panel,
    print_warning,
    prompt_choice,
    STYLES
)
from twilio_manager.core.messaging import get_recent_contacts

class SelectRecipientMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recent_contacts = None
        self.selected_number = None
        self.state = 'main'  # main, manual, contacts

    def show(self):
        """Display menu to select a recipient number."""
        self.state = 'main'
        options = {
            "1": "Enter phone number manually",
            "2": "Select from recent contacts"
        }
        
        self.display(
            title="Select Recipient",
            emoji="📱",
            options=options
        )
        
        return self.selected_number

    def handle_choice(self, choice):
        """Handle the user's menu selection."""
        if self.state == 'main':
            if choice == "1":
                self.state = 'manual'
                self.handle_manual_entry()
            elif choice == "2":
                self.state = 'contacts'
                self.handle_contacts_selection()
        elif self.state == 'contacts':
            try:
                idx = int(choice) - 1
                self.selected_number = self.recent_contacts[idx]['phoneNumber']
                self.print_success(f"Selected number: {self.selected_number}")
                self.pause_and_return()
            except (ValueError, IndexError):
                self.print_error("Invalid selection")
                self.pause_and_return()

    def handle_manual_entry(self):
        """Handle manual phone number entry."""
        number = prompt_choice("Enter recipient phone number (e.g., +14155559876)", choices=None)
        if number:
            self.selected_number = number
            self.print_success(f"Entered number: {self.selected_number}")
        else:
            self.print_warning("No number entered")
        self.pause_and_return()

    def handle_contacts_selection(self):
        """Handle selection from recent contacts."""
        self.recent_contacts = get_recent_contacts()
        if not self.recent_contacts:
            self.print_warning("No recent contacts found.")
            self.handle_manual_entry()
            return

        options = {}
        for idx, contact in enumerate(self.recent_contacts, 1):
            options[str(idx)] = f"{contact['phoneNumber']} (Last: {contact.get('lastContact', 'N/A')})"

        self.display(
            title="Select from Recent Contacts",
            emoji="📞",
            options=options
        )

    def _display_recent_contacts(self, contacts):
        """Display a table of recent contacts."""
        table = create_table(columns=["#", "Phone Number", "Last Contact", "Direction"])
        
        for idx, contact in enumerate(contacts, 1):
            table.add_row(
                str(idx),
                contact['phoneNumber'],
                contact.get('lastContact', 'N/A'),
                contact.get('lastDirection', 'N/A'),
                style=STYLES['data']
            )
        
        console.print(table)