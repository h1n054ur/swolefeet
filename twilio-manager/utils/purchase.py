from services.api import twilio_request
from config.settings import ACCOUNT_SID
from utils.output import format_search_results, sort_results
from utils.ui import console, print_error, print_success


def purchase_number(phone_number):
    """Attempt to purchase a Twilio number by its E.164 format."""
    console.print(f"\n[bold cyan]🛒 Attempting to purchase number:[/] {phone_number}")

    endpoint = f"Accounts/{ACCOUNT_SID}/IncomingPhoneNumbers.json"
    data = {"PhoneNumber": phone_number}
    response = twilio_request("POST", endpoint, data=data)

    if response and response.status_code == 201:
        print_success(f"Number {phone_number} purchased successfully.")
        return True
    else:
        print_error(f"Failed to purchase number {phone_number}")
        return False


def prompt_to_purchase(results):
    """Prompt user to purchase one or more numbers by index or phone number."""
    if not results:
        console.print("[yellow]⚠️ No numbers available to purchase.[/yellow]")
        return

    working = results

    from rich.console import Group
    from rich.align import Align
    from rich.text import Text
    from rich.panel import Panel

    while True:
        console.print("\n[bold cyan]🔍 Available numbers for purchase:[/bold cyan]\n")
        format_search_results(working)

        menu = "\n".join([
            "1. Sort by phone number",
            "2. Sort by region",
            "3. Sort by capability count",
            "4. Continue to purchase",
            "5. Exit"
        ])

        content = Group(
            Align.center(Text("📘 Twilio CLI Manager", style="bold cyan")),
            Align.center(Text("Choose an action", style="bold green")),
            Text(""),
            Text(menu)
        )

        console.print(Align.center(Panel(content, border_style="green"), vertical="middle"))
        choice = input("> ").strip()

        if choice == "1":
            working = sort_results(working, key="phone_number")
        elif choice == "2":
            working = sort_results(working, key="region")
        elif choice == "3":
            working = sort_results(working, key="capability_count")
        elif choice == "4":
            index = input("\nEnter index or full phone number to purchase: ").strip()
            if index.isdigit():
                index = int(index)
                if 0 <= index < len(working):
                    purchase_number(working[index]["phone_number"])
                else:
                    print_error("Invalid index.")
            elif index.startswith("+"):
                match = next((n for n in working if n["phone_number"] == index), None)
                if match:
                    purchase_number(match["phone_number"])
                else:
                    print_error("Number not found in current list.")
            else:
                print_error("Invalid input.")
        elif choice == "5":
            break
        else:
            print_error("Invalid choice.")
