from rich.prompt import Prompt
from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from utils.ui import console, clear_screen, print_error


def select_option_from_list(title, options):
    """Display a numbered list of options and return the selected value."""
    while True:
        clear_screen()
        header = Group(
            Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
            Align.center(Text(f"🔧 {title}", style="bold green")),
            Text("")
        )
        option_lines = [f"{i + 1}. {opt}" for i, opt in enumerate(options)]
        body = Group(
            header,
            *[Text(line) for line in option_lines],
            Text(""),
            Align.center(Text("Choose an option by number:"))
        )
        console.print(Align.center(Panel(body, border_style="green"), vertical="middle"))
        choice = Prompt.ask("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print_error("Invalid choice. Please try again.")
        input("Press Enter to continue...")
