from twilio_manager.cli.menus.configure_menu import ConfigureMenu

def handle_configure_command():
    """Handle the configuration of phone numbers."""
    ConfigureMenu().show()
