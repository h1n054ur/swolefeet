from rich.table import Table
from rich.prompt import Prompt

from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.core.account import (
    get_account_info,
    list_subaccounts,
    list_api_keys,
    list_sip_trunks,
    list_twiml_apps
)

class AccountInfoMenu(BaseMenu):
    def get_title(self):
        return "👤 Account Info / Balance"

    def get_menu_name(self):
        return "Account Info"

    def get_options(self):
        return [("0", "Back", "🔙")]

    def show(self):
        info = get_account_info()
        if not info:
            self.console.print("[red]Failed to retrieve account information.[/red]")
        else:
            table = Table(title="Account Info")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="white")

            for key, value in info.items():
                table.add_row(key, str(value))
            self.console.print(table)

        Prompt.ask("\nPress Enter to return")
        return True

class SubaccountMenu(BaseMenu):
    def get_title(self):
        return "👥 Subaccount List"

    def get_menu_name(self):
        return "Subaccounts"

    def get_options(self):
        return [("0", "Back", "🔙")]

    def show(self):
        subs = list_subaccounts()
        if not subs:
            self.console.print("[yellow]No subaccounts found.[/yellow]")
        else:
            table = Table(title="Subaccounts", show_lines=True)
            table.add_column("SID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="magenta")

            for sub in subs:
                table.add_row(sub["sid"], sub["friendly_name"], sub["status"])

            self.console.print(table)

        Prompt.ask("\nPress Enter to return")
        return True

class ApiKeyMenu(BaseMenu):
    def get_title(self):
        return "🔑 API Key List"

    def get_menu_name(self):
        return "API Keys"

    def get_options(self):
        return [("0", "Back", "🔙")]

    def show(self):
        keys = list_api_keys()
        if not keys:
            self.console.print("[yellow]No API keys found.[/yellow]")
        else:
            table = Table(title="API Keys", show_lines=True)
            table.add_column("SID", style="cyan")
            table.add_column("Friendly Name", style="green")

            for key in keys:
                table.add_row(key["sid"], key["friendly_name"])

            self.console.print(table)

        Prompt.ask("\nPress Enter to return")
        return True

class SipTrunkMenu(BaseMenu):
    def get_title(self):
        return "🔌 SIP Trunks"

    def get_menu_name(self):
        return "SIP Trunks"

    def get_options(self):
        return [("0", "Back", "🔙")]

    def show(self):
        trunks = list_sip_trunks()
        if not trunks:
            self.console.print("[yellow]No SIP trunks found.[/yellow]")
        else:
            table = Table(title="SIP Trunks", show_lines=True)
            table.add_column("SID", style="cyan")
            table.add_column("Friendly Name", style="green")
            table.add_column("Voice Region", style="magenta")

            for trunk in trunks:
                table.add_row(trunk["sid"], trunk["friendly_name"], trunk.get("voice_region", "—"))

            self.console.print(table)

        Prompt.ask("\nPress Enter to return")
        return True

class TwimlAppMenu(BaseMenu):
    def get_title(self):
        return "🧠 TwiML Applications"

    def get_menu_name(self):
        return "TwiML Apps"

    def get_options(self):
        return [("0", "Back", "🔙")]

    def show(self):
        apps = list_twiml_apps()
        if not apps:
            self.console.print("[yellow]No TwiML applications found.[/yellow]")
        else:
            table = Table(title="TwiML Apps", show_lines=True)
            table.add_column("SID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Voice URL", style="magenta")

            for app in apps:
                table.add_row(app["sid"], app["friendly_name"], app.get("voice_url", "—"))

            self.console.print(table)

        Prompt.ask("\nPress Enter to return")
        return True