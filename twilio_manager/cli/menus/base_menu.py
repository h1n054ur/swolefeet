from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

class BaseMenu(ABC):
    def __init__(self, title: str, emoji: str = "📘"):
        self.console = Console()
        self.title = title
        self.emoji = emoji
        self._options: List[Dict[str, Any]] = []

    def add_option(self, key: str, label: str, handler: callable, emoji: str = "") -> None:
        """Add a menu option"""
        self._options.append({
            "key": key,
            "label": label,
            "handler": handler,
            "emoji": emoji
        })

    def clear_screen(self) -> None:
        """Clear the terminal screen"""
        self.console.clear()

    def show_title(self) -> None:
        """Display the menu title"""
        self.console.print(Panel.fit(
            f"[bold cyan]{self.emoji} {self.title}[/bold cyan]",
            title=self.title
        ))

    def show_options(self) -> None:
        """Display all menu options"""
        for option in self._options:
            emoji = f"{option['emoji']} " if option['emoji'] else ""
            self.console.print(
                f"[bold magenta]{option['key']}.[/bold magenta] {emoji}{option['label']}"
            )
        self.console.print()

    def get_valid_choices(self) -> List[str]:
        """Get list of valid choice keys"""
        return [opt["key"] for opt in self._options]

    def handle_choice(self, choice: str) -> bool:
        """Handle a menu choice. Returns True if should exit menu."""
        for option in self._options:
            if option["key"] == choice:
                return option["handler"]()
        return False

    def show(self) -> None:
        """Display the menu and handle user input"""
        while True:
            self.clear_screen()
            self.show_title()
            self.show_options()

            choices = self.get_valid_choices()
            choice = Prompt.ask(
                "Choose an option",
                choices=choices,
                default=choices[-1]  # Usually the exit/back option
            )

            if self.handle_choice(choice):
                break

class SubMenu(BaseMenu):
    """A menu that returns to parent menu"""
    def __init__(self, title: str, emoji: str = "📘"):
        super().__init__(title, emoji)
        # Add back option by default
        self.add_option("0", "🔙 Back", lambda: True, "")

class SearchResultsMenu(BaseMenu):
    """Specialized menu for displaying search results with pagination"""
    def __init__(self, title: str, results: List[dict], page_size: int = 50):
        super().__init__(title, "🔍")
        self.results = results
        self.page_size = page_size
        self.current_page = 1
        self.total_pages = (len(results) + page_size - 1) // page_size

    def display_results_page(self) -> None:
        """Override this method to customize how results are displayed"""
        pass

    def show(self) -> None:
        """Override to implement pagination logic"""
        while True:
            self.clear_screen()
            self.show_title()
            self.display_results_page()

            # Build navigation options
            choices = ["0"]  # Always include exit
            if self.total_pages > 1:
                if self.current_page > 1:
                    choices.extend(["P", "p"])
                if self.current_page < self.total_pages:
                    choices.extend(["N", "n"])

            # Add current page item numbers as valid choices
            start_idx = (self.current_page - 1) * self.page_size
            end_idx = min(start_idx + self.page_size, len(self.results))
            choices.extend([str(i) for i in range(start_idx + 1, end_idx + 1)])

            selection = Prompt.ask(
                "Select an option",
                choices=choices,
                show_choices=False,
                default="0"
            )

            if selection == "0":
                break
            elif selection.upper() == "P" and self.current_page > 1:
                self.current_page -= 1
            elif selection.upper() == "N" and self.current_page < self.total_pages:
                self.current_page += 1
            elif selection.isdigit():
                idx = int(selection) - 1
                if self.handle_item_selection(idx):
                    break

    def handle_item_selection(self, index: int) -> bool:
        """Override this to handle item selection. Return True to exit menu."""
        return False