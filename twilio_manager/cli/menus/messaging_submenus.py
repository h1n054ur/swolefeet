from rich.table import Table
from rich.prompt import Prompt, Confirm

from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.core.messaging import send_message, get_recent_contacts
from twilio_manager.core.phone_numbers import get_active_numbers

class SendMessageMenu(BaseMenu):
    def get_title(self):
        return "✉️ Send a Message"

    def get_menu_name(self):
        return "Send Message"

    def get_options(self):
        return []  # This menu uses a custom flow

    def display_active_numbers(self, numbers):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim")
        table.add_column("Phone Number", style="cyan")
        table.add_column("Friendly Name", style="green")

        for idx, number in enumerate(numbers, 1):
            table.add_row(
                str(idx),
                number['phoneNumber'],
                number.get('friendlyName', 'N/A')
            )
        
        self.console.print(table)

    def display_recent_contacts(self, contacts):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim")
        table.add_column("Phone Number", style="cyan")
        table.add_column("Last Contact", style="green")

        for idx, contact in enumerate(contacts, 1):
            table.add_row(
                str(idx),
                contact['phoneNumber'],
                contact.get('lastContact', 'N/A')
            )
        
        self.console.print(table)

    def show(self):
        self.clear_screen()

        # Get list of active numbers
        active_numbers = get_active_numbers()
        
        if not active_numbers:
            self.show_error("No active numbers found in your account.")
            self.wait_for_input()
            return True

        # Select sender number
        self.console.print("\n[bold]Select a number to send from:[/bold]")
        self.display_active_numbers(active_numbers)

        max_index = len(active_numbers)
        selection = self.get_choice(
            [str(i) for i in range(max_index + 1)],
            prompt="\nSelect a number (0 to cancel)",
            default="0"
        )

        if selection == "0":
            self.show_warning("Message cancelled.")
            return True

        from_number = active_numbers[int(selection) - 1]['phoneNumber']

        # Get recent contacts
        recent_contacts = get_recent_contacts()
        
        # Select recipient
        self.console.print("\n[bold]Select recipient:[/bold]")
        self.print_option("1", "Choose from recent contacts")
        self.print_option("2", "Enter new number")
        
        recipient_choice = self.get_choice(["1", "2"])
        
        if recipient_choice == "1" and recent_contacts:
            self.console.print("\n[bold]Recent Contacts:[/bold]")
            self.display_recent_contacts(recent_contacts)
            
            max_contact_index = len(recent_contacts)
            contact_selection = self.get_choice(
                [str(i) for i in range(max_contact_index + 1)],
                prompt="\nSelect a contact (0 to enter new number)",
                default="0"
            )
            
            if contact_selection == "0":
                to_number = Prompt.ask("Enter recipient's number (E.164 format, e.g., +14155559876)")
            else:
                to_number = recent_contacts[int(contact_selection) - 1]['phoneNumber']
        else:
            to_number = Prompt.ask("Enter recipient's number (E.164 format, e.g., +14155559876)")

        # Get message body
        body = Prompt.ask("\nMessage body")

        # Show summary and confirm
        self.console.print("\n[bold]Message Summary:[/bold]")
        self.console.print(f"From: [cyan]{from_number}[/cyan]")
        self.console.print(f"To: [cyan]{to_number}[/cyan]")
        self.console.print(f"Message:\n[green]{body}[/green]\n")

        confirm = Confirm.ask("Send this message?")
        if not confirm:
            self.show_warning("Message not sent.")
            return True

        success = send_message(from_number, to_number, body)

        if success:
            self.show_success(f"Message sent successfully to {to_number}!")
        else:
            self.show_error(f"Failed to send message to {to_number}.")

        self.wait_for_input()
        return True