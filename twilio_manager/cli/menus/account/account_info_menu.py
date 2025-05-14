from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_error,
    prompt_choice,
    STYLES
)
from twilio_manager.core.account import get_account_info

class AccountInfoMenu(BaseMenu):
    def show(self):
        """Display account information and balance."""
        info = get_account_info()
        if not info:
            print_error("Failed to retrieve account information.")
        else:
            table = create_table(columns=["Field", "Value"], title="Account Info")
            for key, value in info.items():
                table.add_row(key, str(value), style=STYLES['data'])
            console.print(table)

        prompt_choice("\nPress Enter to return", choices=[""], default="")