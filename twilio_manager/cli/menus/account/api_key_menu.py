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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api_keys = None

    def show(self):
        """Display list of API keys."""
        self.api_keys = list_api_keys()
        if not self.api_keys:
            self.print_warning("No API keys found.")
            self.pause_and_return()
            return

        self._display_api_keys()
        options = {"0": "Return to menu"}
        self.display(
            title="API Keys",
            emoji="🔑",
            options=options
        )

    def _display_api_keys(self):
        """Display API keys in a table."""
        table = create_table(columns=["SID", "Friendly Name"], title="API Keys")
        for key in self.api_keys:
            table.add_row(
                key["sid"],
                key["friendly_name"],
                style=STYLES['data']
            )
        console.print(table)

    def handle_choice(self, choice):
        """Handle menu selection."""
        self.return_to_parent()