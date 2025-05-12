# utils/output.py

from rich.console import Console
from rich.table import Table
from rich.box import SIMPLE
import json
import csv

console = Console()


def format_search_results(results):
    if not results:
        console.print("\n[red]❌ No results found.[/red]")
        return

    table = Table(title=f"🎯 {len(results)} Search Result(s)", box=SIMPLE, header_style="bold magenta")
    table.add_column("#", justify="right")
    table.add_column("Phone Number", style="cyan")
    table.add_column("Locality", style="white")
    table.add_column("Region", style="white")
    table.add_column("Capabilities", style="green")

    for i, r in enumerate(results, 1):
        table.add_row(
            str(i),
            r.get("phone_number", "(n/a)"),
            r.get("locality", "(n/a)"),
            r.get("region", "(n/a)"),
            ", ".join(r.get("capabilities", []))
        )

    console.print(table)


def format_manage_results(results):
    if not results:
        console.print("\n[red]❌ No active numbers found.[/red]")
        return

    table = Table(title=f"📱 {len(results)} Active Number(s)", box=SIMPLE, header_style="bold magenta")
    table.add_column("#", justify="right")
    table.add_column("Phone Number", style="cyan")
    table.add_column("Friendly", style="white")
    table.add_column("Capabilities", style="green")

    for i, r in enumerate(results, 1):
        table.add_row(
            str(i),
            r.get("phone_number", "(n/a)"),
            r.get("friendly", "(unnamed)"),
            ", ".join(r.get("capabilities", []))
        )

    console.print(table)


def sort_results(results, key="phone_number"):
    return sorted(results, key=lambda x: x.get(key) or "")


def filter_by_capability(results, capability):
    capability = capability.upper()
    return [
        r for r in results
        if capability in [c.upper() for c in r.get("capabilities", [])]
    ]


def save_results_to_csv(results, filename="results.csv"):
    if not results:
        console.print("[yellow]⚠️ No data to save.[/yellow]")
        return
    keys = results[0].keys()
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
        console.print(f"[green]✅ Results saved to [bold]{filename}[/bold][/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to save CSV: {e}[/red]")


def save_results_to_json(results, filename="results.json"):
    if not results:
        console.print("[yellow]⚠️ No data to save.[/yellow]")
        return
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        console.print(f"[green]✅ Results saved to [bold]{filename}[/bold][/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to save JSON: {e}[/red]")


# Legacy alias for compatibility
format_results = format_search_results
