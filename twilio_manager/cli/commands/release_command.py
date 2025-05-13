from twilio_manager.cli.menus.release_menu import ReleaseMenu

def handle_release_command():
    """Handle the release of a phone number."""
    ReleaseMenu().show()
