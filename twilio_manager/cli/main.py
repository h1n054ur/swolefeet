from twilio_manager.cli.menus.main_menu import MainMenu
from twilio_manager.shared.ui.styling import console, clear_screen
import sys

def run_cli():
    try:
        clear_screen()
        main_menu = MainMenu()
        main_menu.show()
    except KeyboardInterrupt:
        console.print("\n[red]Exited by user.[/red]")
        sys.exit(0)

if __name__ == "__main__":
    run_cli()
