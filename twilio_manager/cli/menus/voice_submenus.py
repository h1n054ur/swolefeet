from rich.table import Table
from rich.prompt import Prompt, Confirm

from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.core.voice import make_call
from twilio_manager.core.phone_numbers import get_active_numbers
from twilio_manager.core.messaging import get_recent_contacts

class MakeCallMenu(BaseMenu):
    def get_title(self):
        return "📞 Make a Voice Call"

    def get_menu_name(self):
        return "Make Call"

    def get_options(self):
        return []  # This menu uses a custom flow

    def display_phone_numbers(self, numbers):
        """Display a table of available phone numbers."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", justify="right")
        table.add_column("Phone Number", style="cyan")
        table.add_column("Friendly Name", style="green")
        table.add_column("Voice Enabled", style="yellow")

        for idx, number in enumerate(numbers, 1):
            voice_enabled = "✓" if number.get('capabilities', {}).get('voice', False) else "✗"
            table.add_row(
                str(idx),
                number['phoneNumber'],
                number.get('friendlyName', 'N/A'),
                voice_enabled
            )
        
        self.console.print(table)

    def display_recent_contacts(self, contacts):
        """Display a table of recent contacts."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", justify="right")
        table.add_column("Phone Number", style="cyan")
        table.add_column("Last Contact", style="green")
        table.add_column("Direction", style="yellow")

        for idx, contact in enumerate(contacts, 1):
            table.add_row(
                str(idx),
                contact['phoneNumber'],
                contact.get('lastContact', 'N/A'),
                contact.get('lastDirection', 'N/A')
            )
        
        self.console.print(table)

    def show(self):
        self.clear_screen()

        # Get active numbers with voice capability
        active_numbers = [n for n in get_active_numbers() if n.get('capabilities', {}).get('voice', False)]
        
        if not active_numbers:
            self.show_error("No voice-enabled numbers found in your account.")
            self.wait_for_input()
            return True

        # Select sender number
        self.console.print("\n[bold]Select a number to call from:[/bold]")
        self.display_phone_numbers(active_numbers)

        max_index = len(active_numbers)
        selection = self.get_choice(
            [str(i) for i in range(max_index + 1)],
            prompt="\nSelect a number (0 to cancel)",
            default="0"
        )

        if selection == "0":
            self.show_warning("Call cancelled.")
            return True

        from_number = active_numbers[int(selection) - 1]['phoneNumber']

        # Get recipient number
        self.console.print("\n[bold]Select recipient:[/bold]")
        self.print_option("1", "Enter phone number manually")
        self.print_option("2", "Select from recent contacts")
        
        recipient_choice = self.get_choice(["1", "2"])
        
        if recipient_choice == "1":
            to_number = Prompt.ask("Enter recipient phone number (e.g., +14155559876)")
        else:
            recent_contacts = get_recent_contacts()
            if not recent_contacts:
                self.show_warning("No recent contacts found.")
                to_number = Prompt.ask("Enter recipient phone number (e.g., +14155559876)")
            else:
                self.console.print("\n[bold]Select from recent contacts:[/bold]")
                self.display_recent_contacts(recent_contacts)
                
                contact_max = len(recent_contacts)
                contact_selection = self.get_choice(
                    [str(i) for i in range(contact_max + 1)],
                    prompt="\nSelect a contact (0 to enter manually)",
                    default="0"
                )
                
                if contact_selection == "0":
                    to_number = Prompt.ask("Enter recipient phone number (e.g., +14155559876)")
                else:
                    to_number = recent_contacts[int(contact_selection) - 1]['phoneNumber']

        # Get voice URL with default options
        self.console.print("\n[bold]Select voice response:[/bold]")
        self.print_option("1", "Default greeting")
        self.print_option("2", "Custom TwiML URL")
        
        url_choice = self.get_choice(["1", "2"])
        
        if url_choice == "1":
            voice_url = "https://handler.twilio.com/twiml/default-greeting"
        else:
            voice_url = Prompt.ask("Enter TwiML URL")

        # Confirm and make call
        self.console.print("\n[bold]Review call details:[/bold]")
        self.console.print(f"From: [green]{from_number}[/green]")
        self.console.print(f"To: [cyan]{to_number}[/cyan]")
        self.console.print(f"Voice URL: [yellow]{voice_url}[/yellow]")

        confirm = Confirm.ask("\nPlace this call?")
        if not confirm:
            self.show_warning("Call cancelled.")
            return True

        success = make_call(from_number, to_number, voice_url)

        if success:
            self.show_success("Call initiated successfully!")
        else:
            self.show_error("Failed to place the call.")

        self.wait_for_input()
        return True