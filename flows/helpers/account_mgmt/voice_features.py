# flows/helpers/account_mgmt/voice_features.py

from utils.ui import console, clear_screen
from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich.align import Align

from .voice_settings import handle_voice_settings_menu
from .voice_call import handle_outbound_call
from .voice_recordings import handle_call_recordings
from .voice_conference import handle_conference_calls
from .voice_ivr import handle_ivr_menu

def handle_voice_features_menu():
    while True:
        clear_screen()

        content = Group(
            Text("📞 Voice Features", style="bold cyan", justify="center"),
            Text("Available Options", style="bold green", justify="center"),
            Text(""),
            Text("1. Make Outbound Calls"),
            Text("2. Access Call Recordings"),
            Text("3. Host Conference Calls"),
            Text("4. Interactive Voice Response (IVR)"),
            Text("5. Voice Settings"),
            Text("6. Back"),
            Text(""),
            Text("Enter your choice (1-6): [1/2/3/4/5/6]", justify="center")
        )

        panel = Panel(content, border_style="green", padding=(1, 4))
        console.print(Align.center(panel, vertical="middle"))

        choice = console.input("\n> ").strip()

        if choice == "1":
            handle_outbound_call()
        elif choice == "2":
            handle_call_recordings()
        elif choice == "3":
            handle_conference_calls()
        elif choice == "4":
            handle_ivr_menu()
        elif choice == "5":
            handle_voice_settings_menu()
        elif choice == "6":
            return
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
            console.input("Press Enter to continue...")
