from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from twilio_manager.cli.commands.search_command import handle_search_command
from twilio_manager.cli.commands.purchase_command import handle_purchase_command
from twilio_manager.cli.commands.configure_command import handle_configure_command
from twilio_manager.cli.commands.release_command import handle_release_command

console = Console()

def show_phone_menu():
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]📞 Phone Number Management[/bold cyan]", title="Phone Menu"))

        console.print("[bold magenta]1.[/bold magenta] 🔍 Search Available Numbers")
        console.print("[bold magenta]2.[/bold magenta] 🛒 Purchase a Number")
        console.print("[bold magenta]3.[/bold magenta] ⚙️  Configure a Number")
        console.print("[bold magenta]4.[/bold magenta] 🗑 Release a Number")
        console.print("[bold magenta]0.[/bold magenta] 🔙 Back\n")

        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "0"], default="0")

        if choice == "1":
            handle_search_command()
        elif choice == "2":
            handle_purchase_command()
        elif choice == "3":
            handle_configure_command()
        elif choice == "4":
            handle_release_command()
        elif choice == "0":
            break
