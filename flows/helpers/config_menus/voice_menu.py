# flows/helpers/config_menus/voice_menu.py

from rich.prompt import Prompt
from utils.ui import console, clear_screen, print_error
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from services.phone_config import update_phone_number
from utils.forms import select_option_from_list
from services.api_helpers import get_sip_trunks, get_twiml_apps


def render_submenu(title: str):
    return Group(
        Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
        Align.center(Text(f"🔧 {title}", style="bold green")),
        Text("")
    )


def handle_simple_input(sid, field, prompt_text):
    value = Prompt.ask(prompt_text).strip()
    if not value:
        print_error("Value cannot be empty.")
        input("Press Enter to continue...")
        return
    update_phone_number(sid, {field: value})
    input("Press Enter to continue...")


def handle_select_input(sid, field, options):
    value = select_option_from_list(field, options)
    if field == "VoiceCallerIdLookup":
        value = "true" if value.lower() == "yes" else "false"
    update_phone_number(sid, {field: value})
    input("Press Enter to continue...")


def handle_twiml_app(sid):
    apps = get_twiml_apps()
    if not apps:
        print_error("No TwiML Applications found.")
        input("Press Enter to continue...")
        return
    options = [f"{a['friendly_name']} ({a['sid']})" for a in apps]
    selected = select_option_from_list("TwiML App", options)
    sid_value = selected.split("(")[-1].replace(")", "").strip()
    update_phone_number(sid, {"VoiceApplicationSid": sid_value})
    input("Press Enter to continue...")


def handle_sip_trunk(sid):
    trunks = get_sip_trunks()
    if not trunks:
        print_error("No SIP Trunks found.")
        input("Press Enter to continue...")
        return
    options = [f"{t['friendly_name']} ({t['sid']})" for t in trunks]
    selected = select_option_from_list("SIP Trunk", options)
    sid_value = selected.split("(")[-1].replace(")", "").strip()
    update_phone_number(sid, {"TrunkSid": sid_value})
    input("Press Enter to continue...")


def advanced_voice_options(sid):
    while True:
        clear_screen()
        content = Group(
            render_submenu("Advanced Voice Options"),
            Text("1. Set SIP Trunk"),
            Text("2. Set TwiML App"),
            Text("3. Toggle Caller ID Lookup"),
            Text("4. Back"),
            Text(""),
            Align.center(Text.from_markup("Choose an option: [bold magenta]1-4[/bold magenta]"))
        )
        console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
        choice = Prompt.ask("\n> ").strip()

        if choice == "1":
            handle_sip_trunk(sid)
        elif choice == "2":
            handle_twiml_app(sid)
        elif choice == "3":
            handle_select_input(sid, "VoiceCallerIdLookup", ["Yes", "No"])
        elif choice == "4":
            break
        else:
            print_error("Invalid choice.")
            input("Press Enter to continue...")


def voice_config_menu(sid):
    while True:
        clear_screen()
        content = Group(
            render_submenu("Voice Settings"),
            Text("1. Set Voice URL"),
            Text("2. Set Voice Method (GET/POST)"),
            Text("3. Set Fallback Voice URL"),
            Text("4. Set Fallback Method"),
            Text("5. Set Status Callback URL"),
            Text("6. Set Status Callback Method"),
            Text("7. Advanced Options"),
            Text("8. Back"),
            Text(""),
            Align.center(Text.from_markup("Choose an option: [bold magenta]1-8[/bold magenta]"))
        )
        console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
        choice = Prompt.ask("\n> ").strip()

        if choice == "1":
            handle_simple_input(sid, "VoiceUrl", "Enter Voice URL")
        elif choice == "2":
            handle_select_input(sid, "VoiceMethod", ["GET", "POST"])
        elif choice == "3":
            handle_simple_input(sid, "VoiceFallbackUrl", "Enter Fallback Voice URL")
        elif choice == "4":
            handle_select_input(sid, "VoiceFallbackMethod", ["GET", "POST"])
        elif choice == "5":
            handle_simple_input(sid, "StatusCallback", "Enter Status Callback URL")
        elif choice == "6":
            handle_select_input(sid, "StatusCallbackMethod", ["GET", "POST"])
        elif choice == "7":
            advanced_voice_options(sid)
        elif choice == "8":
            break
        else:
            print_error("Invalid option.")
            input("Press Enter to continue...")
