# flows/helpers/config_menus/sms_menu.py

from rich.prompt import Prompt
from utils.ui import console, clear_screen, print_error
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from services.phone_config import update_phone_number


def render_submenu(title: str):
    """Render consistent Twilio CLI Manager + submenu title layout."""
    return Group(
        Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
        Align.center(Text(f"🔧 {title}", style="bold green")),
        Text("")
    )


def select_from_options(field_name, options):
    """Display a numbered list of options and return the selected value."""
    while True:
        clear_screen()
        header = render_submenu(field_name)
        option_list = [f"{idx + 1}. {val}" for idx, val in enumerate(options)]
        content = Group(
            header,
            *[Text(line) for line in option_list],
            Text(""),
            Align.center(Text("Choose an option by number:"))
        )
        console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
        choice = Prompt.ask("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print_error("Invalid choice. Please try again.")
        input("Press Enter to continue...")


def sms_config_menu(sid):
    while True:
        clear_screen()
        content = Group(
            render_submenu("Messaging (SMS) Settings"),
            Text("1. Set SMS URL"),
            Text("2. Set SMS Method (GET/POST)"),
            Text("3. Set SMS Fallback URL"),
            Text("4. Set SMS Fallback Method"),
            Text("5. Set SMS Application SID (TwiML App)"),
            Text("6. Back"),
            Text(""),
            Align.center(Text.from_markup("Choose an option: [bold magenta]1-6[/bold magenta]"))
        )
        console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
        choice = Prompt.ask("\n> ").strip()

        if choice == "6":
            break

        field_map = {
            "1": ("SmsUrl", "Enter SMS URL"),
            "2": ("SmsMethod", ["GET", "POST"]),
            "3": ("SmsFallbackUrl", "Enter SMS Fallback URL"),
            "4": ("SmsFallbackMethod", ["GET", "POST"]),
            "5": ("SmsApplicationSid", "Enter SMS App SID")
        }

        if choice not in field_map:
            print_error("Invalid option.")
            input("Press Enter to continue...")
            continue

        field, prompt_or_options = field_map[choice]

        if isinstance(prompt_or_options, list):
            value = select_from_options(field, prompt_or_options)
        else:
            value = Prompt.ask(prompt_or_options).strip()
            if not value:
                print_error("Value cannot be empty.")
                input("Press Enter to continue...")
                continue

        update_phone_number(sid, {field: value})
        input("Press Enter to continue...")
