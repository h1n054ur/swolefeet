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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.account_info = None

    def show(self):
        """Display account information and balance."""
        self.account_info = get_account_info()
        if not self.account_info:
            self.print_error("Failed to retrieve account information.")
            self.pause_and_return()
            return

        self._display_account_info()
        options = {"0": "Return to menu"}
        self.display(
            title="Account Information",
            emoji="💳",
            options=options
        )

    def _display_account_info(self):
        """Display account information in a table."""
        table = create_table(columns=["Field", "Value"], title="Account Info")
        for key, value in self.account_info.items():
            table.add_row(key, str(value), style=STYLES['data'])
        console.print(table)

    def handle_choice(self, choice):
        """Handle menu selection."""
        self.return_to_parent()