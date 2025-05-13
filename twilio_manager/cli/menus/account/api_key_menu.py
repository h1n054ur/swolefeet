from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_warning,
    prompt_choice,
    STYLES
)
from twilio_manager.core.account import list_api_keys

class ApiKeyMenu(BaseMenu):
    def show(self):
        """Display list of API keys."""
        keys = list_api_keys()
        if not keys:
            print_warning("No API keys found.")
        else:
            table = create_table(columns=["SID", "Friendly Name"], title="API Keys")
            for key in keys:
                table.add_row(
                    key["sid"],
                    key["friendly_name"],
                    style=STYLES['data']
                )
            console.print(table)

        prompt_choice("\nPress Enter to return", choices=[""], default="")