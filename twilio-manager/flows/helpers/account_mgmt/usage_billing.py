from twilio.rest import Client
from config.settings import ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET
from utils.ui import console, clear_screen
from rich.console import Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.box import SIMPLE_HEAVY

client = Client(API_KEY_SID, API_KEY_SECRET, ACCOUNT_SID)

def handle_usage_billing_menu():
    while True:
        clear_screen()

        content = Group(
            Text("📊 Usage & Billing", style="bold cyan", justify="center"),
            Text("Usage Menu", style="bold green", justify="center"),
            Text(""),
            Text("1. View Total Usage by Category"),
            Text("2. View Daily Usage Summary"),
            Text("3. View Current Balance"),
            Text("4. Back"),
            Text(""),
            Text("Enter your choice (1-4): [1/2/3/4]", justify="center")
        )

        panel = Panel(content, border_style="green", padding=(1, 4))
        console.print(Align.center(panel, vertical="middle"))

        choice = console.input("\n> ").strip()

        if choice == "1":
            show_total_usage_by_category()
        elif choice == "2":
            show_daily_usage_summary()
        elif choice == "3":
            show_account_balance()
        elif choice == "4":
            return
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
            console.input("\n[cyan]Press Enter to return...[/cyan]")

def show_total_usage_by_category():
    clear_screen()
    table = Table(
        title="📦 Total Usage by Category (All Time)",
        header_style="bold cyan",
        border_style="cyan",
        box=SIMPLE_HEAVY,
        padding=(0, 1)
    )
    table.add_column("Category", style="magenta", no_wrap=True)
    table.add_column("Usage", style="magenta")
    table.add_column("Price (USD)", style="magenta")

    try:
        records = client.usage.records.all_time.list(limit=10)
        for record in records:
            table.add_row(
                record.category or "N/A",
                record.usage or "-",
                f"${record.price or '0.00'}"
            )

        content = Group(
            Align.center(table),
            Text(""),
            Text("Press Enter to return to Usage Menu...", style="white", justify="center")
        )
        panel = Panel(content, border_style="green", padding=(1, 2))
        console.print(Align.center(panel, vertical="middle"))
    except Exception as e:
        console.print(f"[red]Error fetching usage data: {e}[/red]")

    console.input()

def show_daily_usage_summary():
    clear_screen()
    table = Table(
        title="📅 Daily Usage Summary (Last 10 Days)",
        header_style="bold cyan",
        border_style="cyan",
        box=SIMPLE_HEAVY,
        padding=(0, 1)
    )
    table.add_column("Date", style="magenta")
    table.add_column("Category", style="magenta")
    table.add_column("Usage", style="magenta")
    table.add_column("Price (USD)", style="magenta")

    try:
        usage_records = client.usage.records.daily.list(limit=10)
        for record in usage_records:
            table.add_row(
                str(record.start_date),
                record.category or "N/A",
                record.usage or "-",
                f"${record.price or '0.00'}"
            )

        content = Group(
            Align.center(table),
            Text(""),
            Text("Press Enter to return to Usage Menu...", style="white", justify="center")
        )
        panel = Panel(content, border_style="green", padding=(1, 2))
        console.print(Align.center(panel, vertical="middle"))
    except Exception as e:
        console.print(f"[red]Error fetching daily usage: {e}[/red]")

    console.input()

def show_account_balance():
    clear_screen()
    try:
        balance = client.api.balance.fetch()
        content = Group(
            Text("💰 Current Balance", style="bold cyan", justify="center"),
            Text(""),
            Text(f"Balance: ${balance.balance}", style="white", justify="center"),
            Text(f"Currency: {balance.currency}", style="white", justify="center"),
            Text(""),
            Text("Press Enter to return to Usage Menu...", style="white", justify="center")
        )

        panel = Panel(content, border_style="green", padding=(1, 2))
        console.print(Align.center(panel, vertical="middle"))
    except Exception as e:
        console.print(f"[red]Failed to fetch balance: {e}[/red]")

    console.input()

