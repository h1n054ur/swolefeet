# main.py

import os
from flows.manage_flow import handle_manage_flow
from flows.search_flow import handle_search_flow
from flows.account_management_flow import handle_account_management_flow
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()

def clear_screen():
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass

def main():
    while True:
        clear_screen()

        content = Group(
            Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
            Align.center(Text("Main Menu", style="bold green")),
            Text(""),
            Text("1. Search for new numbers"),
            Text("2. Manage active numbers"),
            Text("3. Account Management"),
            Text("4. Exit"),
            Text(""),
            Text("Enter your choice (1-4): [1/2/3/4]")
        )

        panel = Panel(content, border_style="green", padding=(1, 4))
        console.print(Align.center(panel, vertical="middle"))

        choice = console.input("\n> ").strip()

        if choice == "1":
            result = handle_search_flow()
            if result == "restart":
                continue
        elif choice == "2":
            handle_manage_flow()
        elif choice == "3":
            result = handle_account_management_flow()
            if result == "restart":
                continue
            clear_screen()  # <== this clears leftover input
        elif choice == "4":
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")

if __name__ == "__main__":
    main()
