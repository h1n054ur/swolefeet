# flows/manage_flow.py

from services.twilio_numbers import get_active_numbers
from utils.ui import console, clear_screen, print_header, print_error
from utils.common import is_windows
from rich.table import Table
from rich.box import SIMPLE
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
from rich.console import Group
from rich.text import Text

from flows.helpers.manage_actions import handle_number_action


def display_number_table(numbers):
    """Create a formatted Rich table of active numbers."""
    table = Table(show_header=True, header_style="bold magenta", box=SIMPLE)
    table.add_column("#", style="cyan", width=4)
    table.add_column("Phone Number", style="white", width=20)
    table.add_column("Friendly", style="green", width=20)
    table.add_column("Capabilities", style="bright_white", width=25)

    for idx, number in enumerate(numbers, start=1):
        friendly = number.get("friendly_name", "")
        caps = ", ".join([cap.upper() for cap, val in number["capabilities"].items() if val])
        table.add_row(str(idx), number["phone_number"], friendly, caps)

    return table


def handle_manage_flow():
    """Flow to display and select a number to manage."""
    clear_screen()
    numbers = get_active_numbers()

    if not numbers:
        console.print("[yellow]No active numbers found.[/yellow]")
        input("Press Enter to return...")
        return

    table = display_number_table(numbers)

    content = Group(
        Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
        Align.center(Text("Manage Active Numbers", style="bold green")),
        Text(""),
        table,
        Text(""),
        Align.center(Text("Enter number # to manage (or 'q' to quit):"))
    )

    console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
    choice = console.input("\n> ").strip()

    if choice.lower() == "q":
        return
    if not choice.isdigit():
        print_error("Invalid input. Please enter a number.")
        input("Press Enter to return...")
        return

    idx = int(choice)
    if 1 <= idx <= len(numbers):
        handle_number_action(numbers[idx - 1])
    else:
        print_error("Invalid selection.")
        input("Press Enter to return...")
