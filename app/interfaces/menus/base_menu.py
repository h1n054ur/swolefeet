"""Shared base class for all CLI menus."""

class BaseMenu:
    def show_header(self, title: str):
        print("=" * 50)
        print(f"{title.center(50)}")
        print("=" * 50)

    def prompt_back_option(self) -> bool:
        choice = input("\nEnter 'b' to go back or any key to continue: ").lower()
        return choice == 'b'

    def clear_screen(self):
        print("\033[H\033[J", end="")  # ANSI escape sequence to clear terminal
