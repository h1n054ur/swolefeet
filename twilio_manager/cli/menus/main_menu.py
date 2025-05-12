from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from twilio_manager.cli.menus.phone_menu import show_phone_menu
from twilio_manager.cli.menus.messaging_menu import show_messaging_menu
from twilio_manager.cli.menus.voice_menu import show_voice_menu
from twilio_manager.cli.menus.account_menu import show_account_menu
from twilio_manager.cli.menus.advanced_menu import show_advanced_menu

console = Console()

def show_main_menu():
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]📘 Twilio CLI Manager[/bold cyan]", title="Main Menu"))

        console.print("[bold magenta]1.[/bold magenta] 📞 Phone Numbers")
        console.print("[bold magenta]2.[/bold magenta] 📨 Messaging")
        console.print("[bold magenta]3.[/bold magenta] 📞 Voice")
        console.print("[bold magenta]4.[/bold magenta] 🧾 Account")
        console.print("[bold magenta]5.[/bold magenta] 🧠 Advanced Features")
        console.print("[bold magenta]0.[/bold magenta] ❌ Exit\n")

        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "0"], default="0")

        if choice == "1":
            show_phone_menu()
        elif choice == "2":
            show_messaging_menu()
        elif choice == "3":
            show_voice_menu()
        elif choice == "4":
            show_account_menu()
        elif choice == "5":
            show_advanced_menu()
        elif choice == "0":
            console.print("\n[green]Goodbye![/green]")
            break
