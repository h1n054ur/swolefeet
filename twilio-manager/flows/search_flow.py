from utils.ui import clear_screen, print_header, console, print_info
from utils.output import (
    format_search_results,
    sort_results,
    save_results_to_csv,
    save_results_to_json,
    filter_by_capability,
)
from utils.purchase import prompt_to_purchase
from flows.helpers.search_prompts import get_search_parameters
from flows.helpers.search_actions import perform_digit_search, perform_region_search
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align
from rich.console import Group
from rich.text import Text
import shutil


def handle_search_flow():
    clear_screen()
    print_header("🔍 Start Number Search")

    # Step 1: Prompt user for country, capability, and search mode
    params = get_search_parameters()
    if not params:
        return
    country_code, selected_cap, search_mode = params

    # Step 2: Execute appropriate search
    if search_mode == "digits":
        results = perform_digit_search(country_code, selected_cap)
    else:
        results = perform_region_search(country_code, selected_cap)

    if not results:
        console.print("[red]❌ No numbers found.[/red]")
        input("Press Enter to return to the main menu...")
        return

    # Step 3: Show interactive menu
    while True:
        clear_screen()

        menu = "\n".join([
            "1. View formatted results",
            "2. Sort by phone number",
            "3. Sort by locality",
            "4. Filter by capability (e.g. SMS, VOICE)",
            "5. Save to CSV",
            "6. Save to JSON",
            "7. Purchase a number",
            "8. Back to main menu"
        ])

        content = Group(
            Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
            Align.center(Text("Results Menu", style="bold green")),
            Text(""),
            Text(menu),
            Text(""),
            Text.from_markup("Enter your choice (1-8): [bold magenta]1/2/3/4/5/6/7/8[/bold magenta]")
        )

        console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
        choice = console.input("\n> ").strip()

        if choice == "1":
            console.print(format_search_results(results))
            input("\nPress Enter to return to the menu...")

        elif choice == "2":
            results = sort_results(results, key="phone_number")
            console.print(format_search_results(results))
            console.print("[cyan]Sorted by phone number.[/cyan]")
            input("Press Enter to return...")

        elif choice == "3":
            results = sort_results(results, key="locality")
            console.print(format_search_results(results))
            console.print("[cyan]Sorted by locality.[/cyan]")
            input("Press Enter to return...")

        elif choice == "4":
            width = shutil.get_terminal_size().columns
            prompt_text = "Enter capability to filter by (e.g. SMS, VOICE):"
            padding = (width - len(prompt_text)) // 2
            aligned_prompt = " " * max(padding, 0) + prompt_text
            cap = Prompt.ask(aligned_prompt).strip()
            filtered = filter_by_capability(results, cap)
            if filtered:
                results = filtered
                print_info(f"Results filtered by capability: {cap.upper()}")
            else:
                print_info("No results matched selected capability.")
            input("Press Enter to return...")

        elif choice == "5":
            save_results_to_csv(results)
            input("Press Enter to return...")

        elif choice == "6":
            save_results_to_json(results)
            input("Press Enter to return...")

        elif choice == "7":
            prompt_to_purchase(results)
            input("Press Enter to return...")

        elif choice == "8":
            break
