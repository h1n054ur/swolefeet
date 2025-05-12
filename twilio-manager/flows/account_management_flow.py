# flows/account_management_flow.py

from flows.helpers.account_mgmt.usage_billing import handle_usage_billing_menu
from flows.helpers.account_mgmt.voice_features import handle_voice_features_menu
from utils.ui import console, clear_screen
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

def handle_account_management_flow():
    clear_screen()

    content = Group(
        Align.center(Text("🔐 Account Management", style="bold cyan")),
        Align.center(Text("Select a category", style="bold green")),
        Text(""),
        Text("1. Usage & Billing"),
        Text("2. Voice Features"),
        Text("3. Messaging"),
        Text("4. Security & Compliance"),
        Text("5. Account & Subaccount Management"),
        Text("6. Developer Tools"),
        Text("7. Back"),
        Text(""),
        Text("Enter your choice (1-7): [1/2/3/4/5/6/7]")
    )

    panel = Panel(content, border_style="green", padding=(1, 4))
    console.print(Align.center(panel, vertical="middle"))

    choice = console.input("\n> ").strip()

    if choice == "1":
        clear_screen()
        handle_usage_billing_menu()
        return "restart"
    elif choice == "2":
        clear_screen()
        handle_voice_features_menu()  # ✅ now from external file
        return "restart"
    elif choice == "3":
        clear_screen()
        handle_messaging_menu()
        return "restart"
    elif choice == "4":
        clear_screen()
        handle_security_compliance_menu()
        return "restart"
    elif choice == "5":
        clear_screen()
        handle_account_subaccount_menu()
        return "restart"
    elif choice == "6":
        clear_screen()
        handle_developer_tools_menu()
        return "restart"
    elif choice == "7":
        return
    else:
        console.print("[red]Invalid choice. Please try again.[/red]")
        console.input("\n[cyan]Press Enter to return...[/cyan]")
        return "restart"

# Remaining placeholder submenus stay the same

def handle_messaging_menu():
    content = Panel.fit(
        Group(
            Align.center(Text("📧 Messaging Menu (Coming Soon)", style="bold cyan")),
            Text(""),
            Align.center(Text("Press Enter to return...", style="white"))
        ),
        border_style="green"
    )
    console.print(Align.center(content, vertical="middle"))
    console.input()

def handle_security_compliance_menu():
    content = Panel.fit(
        Group(
            Align.center(Text("🔐 Security & Compliance Menu (Coming Soon)", style="bold cyan")),
            Text(""),
            Align.center(Text("Press Enter to return...", style="white"))
        ),
        border_style="green"
    )
    console.print(Align.center(content, vertical="middle"))
    console.input()

def handle_account_subaccount_menu():
    content = Panel.fit(
        Group(
            Align.center(Text("🧑‍💼 Account & Subaccount Menu (Coming Soon)", style="bold cyan")),
            Text(""),
            Align.center(Text("Press Enter to return...", style="white"))
        ),
        border_style="green"
    )
    console.print(Align.center(content, vertical="middle"))
    console.input()

def handle_developer_tools_menu():
    content = Panel.fit(
        Group(
            Align.center(Text("🛠️ Developer Tools Menu (Coming Soon)", style="bold cyan")),
            Text(""),
            Align.center(Text("Press Enter to return...", style="white"))
        ),
        border_style="green"
    )
    console.print(Align.center(content, vertical="middle"))
    console.input()
