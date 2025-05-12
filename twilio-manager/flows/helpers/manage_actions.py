from services.twilio_numbers import (
    get_number_properties,
    update_friendly_name,
    release_number
)
from services.twilio_logs import view_call_logs, view_message_logs
from utils.ui import console, clear_screen, print_error, print_success
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.box import SIMPLE
from rich.align import Align
from rich.panel import Panel
from rich.console import Group
from rich.text import Text

# New config submenus
from flows.helpers.config_menus.voice_menu import voice_config_menu
from flows.helpers.config_menus.sms_menu import sms_config_menu
from flows.helpers.config_menus.fax_menu import fax_config_menu


def display_number_properties(sid):
    number = get_number_properties(sid)
    if not number:
        return

    clear_screen()
    console.print("[bold cyan]📇 Phone Number Properties[/bold cyan]")

    table = Table(title="📇 Properties", box=SIMPLE, header_style="bold magenta")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    props = [
        ("SID", number["sid"]),
        ("Phone Number", number["phone_number"]),
        ("Friendly Name", number.get("friendly_name") or "(not set)"),
        ("Voice URL", number.get("voice_url") or "(not set)"),
        ("SMS URL", number.get("sms_url") or "(not set)"),
        ("Status Callback", number.get("status_callback") or "(not set)"),
        ("Capabilities", ", ".join([cap.upper() for cap, enabled in number["capabilities"].items() if enabled])),
    ]

    for label, value in props:
        table.add_row(label, str(value))

    console.print(table)
    input("\nPress Enter to return...")


def handle_number_action(number):
    sid = number["sid"]
    while True:
        clear_screen()

        menu = "\n".join([
            "1. View details",
            "2. Update friendly name",
            "3. View call logs",
            "4. View SMS logs",
            "5. Voice Settings",
            "6. SMS Settings",
            "7. Fax Settings",
            "8. Release number",
            "9. Back"
        ])

        content = Group(
            Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
            Align.center(Text(f"Manage {number['phone_number']}", style="bold green")),
            Text(""),
            Text(menu),
            Text(""),
            Align.center(Text.from_markup("Choose an action: [bold magenta]1-9[/bold magenta]"))
        )

        console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))

        choice = console.input("\n> ").strip().lower()

        if choice == "1":
            display_number_properties(sid)

        elif choice == "2":
            new_name = Prompt.ask("Enter new friendly name").strip()
            if new_name:
                success = update_friendly_name(sid, new_name)
                if success:
                    print_success("Friendly name updated successfully.")
                else:
                    print_error("Failed to update friendly name.")
            input("Press Enter to continue...")

        elif choice == "3":
            view_call_logs(number["phone_number"])

        elif choice == "4":
            view_message_logs(number["phone_number"])

        elif choice == "5":
            voice_config_menu(sid)

        elif choice == "6":
            sms_config_menu(sid)

        elif choice == "7":
            fax_config_menu(sid)

        elif choice == "8":
            if Confirm.ask("Are you sure you want to release this number?", default=False):
                if release_number(sid):
                    print_success("Number released successfully.")
                    break
                else:
                    print_error("Failed to release number.")
            input("Press Enter to continue...")

        elif choice == "9":
            break
