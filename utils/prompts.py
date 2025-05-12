from config.regions import REGIONS
from rich.prompt import Prompt, Confirm
from utils.ui import console, clear_screen
from rich.panel import Panel
from rich.align import Align
from rich.console import Group
from rich.text import Text


def prompt_country_selection():
    clear_screen()
    countries = list(REGIONS.keys())

    country_list = "\n".join(
        f"[cyan]{idx}.[/] {REGIONS[code]['name']} ({code})"
        for idx, code in enumerate(countries, 1)
    )

    content = Group(
        Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
        Align.center(Text("Country Selection", style="bold green")),
        Text(""),
        Text("🌍 Select the country to search in:", style="bold"),
        Text(""),
        Text.from_markup(country_list),
        Text(""),
        Text("Enter choice (e.g. 1, 2, 3):")
    )

    console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
    choice = console.input("\n> ").strip()

    try:
        idx = int(choice)
        if 1 <= idx <= len(countries):
            return countries[idx - 1]
    except ValueError:
        pass

    return prompt_country_selection()


def prompt_capability():
    clear_screen()
    capabilities = ["Voice", "SMS", "MMS"]

    capability_list = "\n".join(
        f"[cyan]{idx}.[/] {cap}" for idx, cap in enumerate(capabilities, 1)
    )

    content = Group(
        Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
        Align.center(Text("Capability Selection", style="bold green")),
        Text(""),
        Text("📡 Select the number capability:", style="bold"),
        Text(""),
        Text.from_markup(capability_list),
        Text(""),
        Text("Enter choice (1-3):")
    )

    console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
    choice = console.input("\n> ").strip()

    try:
        selected = int(choice) - 1
        if 0 <= selected < len(capabilities):
            return capabilities[selected].lower()
    except ValueError:
        pass

    return prompt_capability()


def prompt_search_mode():
    clear_screen()

    content = Group(
        Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
        Align.center(Text("Search Mode", style="bold green")),
        Text(""),
        Text("Do you want to search using digits across the whole country?", style="bold"),
        Text(""),
        Text("Use digit search? (y/n):")
    )

    console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))

    while True:
        response = console.input("\n> ").strip().lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        console.print("[red]Please enter 'y' or 'n'.[/red]")




def prompt_digit_sequence():
    clear_screen()

    content = Group(
        Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
        Align.center(Text("Digit Filter", style="bold green")),
        Text(""),
        Text("Enter digit sequence to search for (minimum 2 digits):", style="bold"),
        Text(""),
        Text("Enter digits:")
    )

    console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
    digits = console.input("\n> ").strip()

    if digits and digits.isdigit() and len(digits) >= 2:
        return digits

    console.print("[red]❌ Invalid input. Minimum 2 digits required.[/red]")
    return None


def prompt_region_selection(country_code):
    clear_screen()
    region_data = REGIONS.get(country_code, {}).get("region_data", {})
    region_names = list(region_data.keys())

    region_list = "\n".join(
        f"[cyan]{idx}.[/] {name}" for idx, name in enumerate(region_names, 1)
    )

    content = Group(
        Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
        Align.center(Text("Region Selection", style="bold green")),
        Text(""),
        Text("🗺️ Select a region:", style="bold"),
        Text(""),
        Text.from_markup(region_list),
        Text(""),
        Text(f"Enter choice (1-{len(region_names)}):")
    )

    console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
    choice = console.input("\n> ").strip()

    try:
        selected = int(choice) - 1
        if 0 <= selected < len(region_names):
            return region_names[selected]
    except ValueError:
        pass

    console.print("[red]❌ Invalid region selection.[/red]")
    return None
