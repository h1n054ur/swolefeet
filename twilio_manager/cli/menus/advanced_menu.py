from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from twilio_manager.cli.commands.manage_account_command import (
    handle_sip_trunk_menu,
    handle_twiml_app_menu
)

console = Console()

def show_advanced_menu():
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]🧠 Advanced Voice Features[/bold cyan]", title="Advanced Menu"))

        console.print("[bold magenta]1.[/bold magenta] 🔌 SIP Trunks")
        console.print("[bold magenta]2.[/bold magenta] 🧠 TwiML Applications")
        # console.print("[bold magenta]3.[/bold magenta] 📥 Inbound Call Settings")  # Optional
        console.print("[bold magenta]0.[/bold magenta] 🔙 Back\n")

        choice = Prompt.ask("Choose an option", choices=["1", "2", "0"], default="0")

        if choice == "1":
            handle_sip_trunk_menu()
        elif choice == "2":
            handle_twiml_app_menu()
        # elif choice == "3":
        #     handle_inbound_settings_menu()
        elif choice == "0":
            break
# Placeholder for advanced_menu.py
