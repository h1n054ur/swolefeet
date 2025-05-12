from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from tqdm import tqdm

from twilio_manager.core.phone_numbers import search_available_numbers

console = Console()

def handle_search_command():
    console.clear()
    console.print(Panel.fit("[bold cyan]🔍 Search Available Numbers[/bold cyan]"))

    country = Prompt.ask("Enter country code", default="US").upper()
    number_type = Prompt.ask("Number type", choices=["local", "mobile", "tollfree"], default="local")
    caps_input = Prompt.ask("Capabilities (comma-separated)", default="SMS,Voice")
    capabilities = [cap.strip().upper() for cap in caps_input.split(",") if cap.strip()]
    pattern = Prompt.ask("Vanity pattern (optional)", default="")

    console.print("\n[bold yellow]Searching...[/bold yellow]")

    # Use tqdm for a simulated loading experience (in real case this would be paginated)
    with tqdm(total=1, desc="🔍 Fetching numbers", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        results = search_available_numbers(country, number_type, capabilities, pattern)
        pbar.update(1)

    if not results:
        console.print("[red]No matching numbers found.[/red]")
        return

    table = Table(title="Available Numbers", show_lines=True)
    table.add_column("SID", style="dim", overflow="fold")
    table.add_column("Phone Number", style="bold")
    table.add_column("Region", style="green")
    table.add_column("Capabilities", style="magenta")

    for number in results:
        caps = ", ".join([cap.upper() for cap, val in number['capabilities'].items() if val])
        table.add_row(
            number.get("sid", "—"),
            number.get("phone_number", "—"),
            number.get("region", "—"),
            caps or "—"
        )

    console.print("\n")
    console.print(table)
    Prompt.ask("\nPress Enter to return")
