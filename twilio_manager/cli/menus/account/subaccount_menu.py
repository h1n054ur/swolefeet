from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_warning,
    prompt_choice,
    STYLES
)
from twilio_manager.core.account import list_subaccounts

class SubaccountMenu(BaseMenu):
    def show(self):
        """Display list of subaccounts."""
        subs = list_subaccounts()
        if not subs:
            print_warning("No subaccounts found.")
        else:
            table = create_table(columns=["SID", "Name", "Status"], title="Subaccounts")
            for sub in subs:
                table.add_row(
                    sub["sid"],
                    sub["friendly_name"],
                    sub["status"],
                    style=STYLES['data']
                )
            console.print(table)

        prompt_choice("\nPress Enter to return", choices=[""], default="")