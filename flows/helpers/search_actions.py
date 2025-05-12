from services.search_engine import search_by_digits, search_by_region
from config.regions import REGIONS
from flows.helpers.search_prompts import get_digit_sequence, get_selected_region
from utils.ui import clear_screen, console
from rich.panel import Panel
from rich.align import Align
from rich.console import Group
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn, MofNCompleteColumn, TaskProgressColumn
from rich.live import Live


def perform_digit_search(country_code, selected_capability):
    digits = get_digit_sequence()
    if digits is None:
        console.print("[red]Digit entry cancelled.[/red]")
        return []

    clear_screen()

    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        expand=True
    )

    task_id = progress.add_task("Searching", total=500)

    def render_panel():
        return Panel(
            Group(
                Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
                Align.center(Text("Digit Search", style="bold green")),
                Text(""),
                Text(f"🔎 Searching for {country_code} numbers containing '{digits}' with {selected_capability.upper()} capability...", style="bold"),
                Text(""),
                progress
            ),
            border_style="green"
        )

    with Live(render_panel(), console=console, refresh_per_second=10):
        return search_by_digits(country_code, selected_capability, digits, silent=False, rich_progress=progress)


def perform_region_search(country_code, selected_capability):
    selected_region = get_selected_region(country_code)
    if selected_region is None:
        console.print("[red]Region selection cancelled.[/red]")
        return []

    region_data = REGIONS[country_code]["region_data"]

    clear_screen()

    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        expand=True
    )

    task_id = progress.add_task("Searching", total=500)

    def render_panel():
        return Panel(
            Group(
                Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
                Align.center(Text("Region Search", style="bold green")),
                Text(""),
                Text(f"🔎 Searching in {selected_region} region with {selected_capability.upper()} capability...", style="bold"),
                Text(""),
                progress
            ),
            border_style="green"
        )

    with Live(render_panel(), console=console, refresh_per_second=10):
        return search_by_region(country_code, selected_capability, region_data, selected_region, silent=False, rich_progress=progress)
