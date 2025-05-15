"""CLI entry point."""

from app.interfaces.menus.main_menu import MainMenu

def main():
    menu = MainMenu()
    menu.show()

if __name__ == "__main__":
    main()
