from twilio_manager.cli.menus.base_menu import BaseMenu
from twilio_manager.shared.ui.styling import (
    console,
    create_table,
    print_warning,
    prompt_choice,
    STYLES
)
from twilio_manager.core.account import list_twiml_apps

class TwimlAppMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.twiml_apps = None

    def show(self):
        """Display list of TwiML applications."""
        self.twiml_apps = list_twiml_apps()
        if not self.twiml_apps:
            self.print_warning("No TwiML applications found.")
            self.pause_and_return()
            return

        self._display_twiml_apps()
        options = {"0": "Return to menu"}
        self.display(
            title="TwiML Applications",
            emoji="🔌",
            options=options
        )

    def _display_twiml_apps(self):
        """Display TwiML applications in a table."""
        table = create_table(
            columns=["SID", "Name", "Voice URL"],
            title="TwiML Apps"
        )
        for app in self.twiml_apps:
            table.add_row(
                app["sid"],
                app["friendly_name"],
                app.get("voice_url", "—"),
                style=STYLES['data']
            )
        console.print(table)

    def handle_choice(self, choice):
        """Handle menu selection."""
        self.return_to_parent()