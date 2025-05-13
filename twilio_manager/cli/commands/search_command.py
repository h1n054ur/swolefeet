from twilio_manager.cli.menus.search_menu import SearchMenu

def handle_search_command():
    """Handle the search for available phone numbers."""
    SearchMenu().show()
