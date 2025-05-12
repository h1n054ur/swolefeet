from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from twilio_manager.cli.commands.manage_account_command import (
    handle_view_account_info,
    handle_subaccount_management,
    handle_api_key_management
)

console = Console()

def show_account_menu():
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]🧾 Account Management[/bold cyan]", title="Account Menu"))

        console.print("[bold magenta]1.[/bold magenta] 👤 View Account Info / Balance")
        console.print("[bold magenta]2.[/bold magenta] 👥 Manage Subaccounts")
        console.print("[bold magenta]3.[/bold magenta] 🔑 Manage API Keys")
        console.print("[bold magenta]0.[/bold magenta] 🔙 Back\n")

        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "0"], default="0")

        if choice == "1":
            handle_view_account_info()
        elif choice == "2":
            handle_subaccount_management()
        elif choice == "3":
            handle_api_key_management()
        elif choice == "0":
            break
# Placeholder for account_menu.py
