"""CLI menu: MainMenu."""

from app.interfaces.menus.base_menu import BaseMenu
from app.interfaces.menus.account_menu import AccountMenu
from app.interfaces.menus.active_numbers_menu import ActiveNumbersMenu
from app.interfaces.menus.search_menu import SearchMenu
from app.interfaces.menus.communications_menu import CommunicationsMenu
from app.interfaces.menus.advanced_menu import AdvancedMenu

class MainMenu(BaseMenu):
    def show(self):
        while True:
            self.show_header("Twilio CLI App - Main Menu")
            print("1. Account Management")
            print("2. Manage Active Numbers")
            print("3. Search for Numbers")
            print("4. Communications")
            print("5. Advanced")
            print("0. Exit")

            choice = input("Select an option: ").strip()
            if choice == "1":
                AccountMenu().show()
            elif choice == "2":
                ActiveNumbersMenu().show()
            elif choice == "3":
                SearchMenu().show()
            elif choice == "4":
                CommunicationsMenu().show()
            elif choice == "5":
                AdvancedMenu().show()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
