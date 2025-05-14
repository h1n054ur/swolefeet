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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.subaccounts = None

    def show(self):
        """Display list of subaccounts."""
        self.subaccounts = list_subaccounts()
        if not self.subaccounts:
            self.print_warning("No subaccounts found.")
            self.pause_and_return()
            return

        self._display_subaccounts()
        options = {"0": "Return to menu"}
        self.display(
            title="Subaccounts",
            emoji="👥",
            options=options
        )

    def _display_subaccounts(self):
        """Display subaccounts in a table."""
        table = create_table(columns=["SID", "Name", "Status"], title="Subaccounts")
        for sub in self.subaccounts:
            table.add_row(
                sub["sid"],
                sub["friendly_name"],
                sub["status"],
                style=STYLES['data']
            )
        console.print(table)

    def handle_choice(self, choice):
        """Handle menu selection."""
        self.return_to_parent()