# flows/helpers/account_mgmt/voice_settings.py

from utils.ui import console, clear_screen
from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich.align import Align

from .voice_trunks import handle_sip_trunks_menu
from .voice_caller_ids import handle_caller_ids_menu
from .voice_twiml_apps import handle_twiml_apps_menu
from .voice_inbound_settings import handle_inbound_call_settings

def handle_voice_settings_menu():
    while True:
        clear_screen()
        content = Group(
            Text("🛠 Voice Settings", style="bold cyan", justify="center"),
            Text("Configure routing, SIP, caller IDs, and apps", style="green"),
            Text(""),
            Text("1. SIP Trunks"),
            Text("2. Caller IDs"),
            Text("3. TwiML Apps"),
            Text("4. Inbound Call Settings"),
            Text("5. Back"),
            Text(""),
            Text("Enter your choice (1-5):", justify="center")
        )
        panel = Panel(content, border_style="green", padding=(1, 4))
        console.print(Align.center(panel, vertical="middle"))

        choice = console.input("\n> ").strip()

        if choice == "1":
            handle_sip_trunks_menu()
        elif choice == "2":
            handle_caller_ids_menu()
        elif choice == "3":
            handle_twiml_apps_menu()
        elif choice == "4":
            handle_inbound_call_settings()
        elif choice == "5":
            return
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
            console.input("Press Enter to continue...")
