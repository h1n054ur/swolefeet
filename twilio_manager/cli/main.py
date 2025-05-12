from twilio_manager.cli.menus.main_menu import show_main_menu
from rich.console import Console
import sys

console = Console()

def run_cli():
    try:
        console.clear()
        console.rule("[bold green]Twilio CLI Manager")
        show_main_menu()
    except KeyboardInterrupt:
        console.print("\n[red]Exited by user.[/red]")
        sys.exit(0)

if __name__ == "__main__":
    run_cli()
