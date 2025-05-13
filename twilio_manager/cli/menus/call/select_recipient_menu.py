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
    def show(self):
        """Display menu to select a recipient number."""
        print_panel("Select recipient:", style='highlight')
        recipient_choice = prompt_choice(
            "Choose an option:\n1. Enter phone number manually\n2. Select from recent contacts",
            choices=["1", "2"],
            default="1"
        )
        
        if recipient_choice == "1":
            return prompt_choice("Enter recipient phone number (e.g., +14155559876)", choices=None)
        
        # Get from recent contacts
        recent_contacts = get_recent_contacts()
        if not recent_contacts:
            print_warning("No recent contacts found.")
            return prompt_choice("Enter recipient phone number (e.g., +14155559876)", choices=None)
        
        print_panel("Select from recent contacts:", style='highlight')
        self._display_recent_contacts(recent_contacts)
        
        contact_max = len(recent_contacts)
        contact_selection = prompt_choice(
            "\nSelect a contact (0 to enter manually)",
            choices=[str(i) for i in range(contact_max + 1)]
        )
        
        if contact_selection == "0":
            return prompt_choice("Enter recipient phone number (e.g., +14155559876)", choices=None)
        
        return recent_contacts[int(contact_selection) - 1]['phoneNumber']

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