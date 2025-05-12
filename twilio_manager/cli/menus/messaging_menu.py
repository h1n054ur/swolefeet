from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from twilio_manager.cli.commands.send_message_command import handle_send_message_command
from twilio_manager.cli.commands.view_logs_command import handle_view_message_logs_command
# from cli.commands.delete_message_command import handle_delete_message_command  # Optional

console = Console()

def show_messaging_menu():
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]📨 Messaging Management[/bold cyan]", title="Messaging Menu"))

        console.print("[bold magenta]1.[/bold magenta] ✉️ Send a Message")
        console.print("[bold magenta]2.[/bold magenta] 📄 View Message Logs")
        # console.print("[bold magenta]3.[/bold magenta] 🗑 Delete a Message")  # Optional
        console.print("[bold magenta]0.[/bold magenta] 🔙 Back\n")

        choice = Prompt.ask("Choose an option", choices=["1", "2", "0"], default="0")

        if choice == "1":
            handle_send_message_command()
        elif choice == "2":
            handle_view_message_logs_command()
        # elif choice == "3":
        #     handle_delete_message_command()
        elif choice == "0":
            break
