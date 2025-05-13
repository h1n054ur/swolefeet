from twilio_manager.shared.ui.styling import (
    clear_screen,
    print_header,
    prompt_choice,
    console,
    STYLES
)
from twilio_manager.shared.constants import MENU_TITLES

class BaseMenu:
    def show(self):
        """Display the menu and handle user interaction.
        
        This method must be implemented by subclasses to define the menu's behavior.
        """
        raise NotImplementedError("Override this method in subclasses")

    def display(self, title, emoji, options):
        """Display the menu and handle user input in a loop.
        
        Args:
            title (str): The title of the menu
            emoji (str): Emoji to display with the title
            options (dict): Dictionary mapping option keys to their descriptions
        """
        while True:
            self.clear()
            self.print_title(title, emoji)
            for key, desc in options.items():
                console.print(f"[bold magenta]{key}.[/bold magenta] {desc}")
            choice = self.get_choice(list(options.keys()))
            if choice == "0":
                break
            self.handle_choice(choice)

    def handle_choice(self, choice):
        """Handle the user's menu choice. Must be implemented by subclasses.
        
        Args:
            choice (str): The user's selected option
            
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Override this method in subclasses")

    def clear(self):
        """Clear the screen."""
        clear_screen()

    def print_title(self, title, emoji=None):
        """Print the menu title with optional emoji.
        
        Args:
            title (str): The title to display
            emoji (str, optional): Emoji to display with the title
        """
        print_header(title, emoji)

    def get_choice(self, choices, prompt="Choose an option", default="0"):
        """Get user input from a list of choices.
        
        Args:
            choices (list): List of valid choices
            prompt (str, optional): Prompt to display
            default (str, optional): Default choice
            
        Returns:
            str: The user's choice
        """
        return prompt_choice(prompt, choices=choices, default=default)

    def print_option(self, key, description, style=STYLES['data']):
        """Print a menu option with consistent styling.
        
        Args:
            key (str): The option key/number
            description (str): The option description
            style (str, optional): Style to apply to the description
        """
        console.print(f"[bold magenta]{key}.[/bold magenta] {description}", style=style)

    def print_info(self, message, style=STYLES['info']):
        """Print an informational message with consistent styling.
        
        Args:
            message (str): The message to display
            style (str, optional): Style to apply to the message
        """
        console.print(message, style=style)

    def print_error(self, message, style=STYLES['error']):
        """Print an error message with consistent styling.
        
        Args:
            message (str): The message to display
            style (str, optional): Style to apply to the message
        """
        console.print(message, style=style)

    def print_success(self, message, style=STYLES['success']):
        """Print a success message with consistent styling.
        
        Args:
            message (str): The message to display
            style (str, optional): Style to apply to the message
        """
        console.print(message, style=style)

    def print_warning(self, message, style=STYLES['warning']):
        """Print a warning message with consistent styling.
        
        Args:
            message (str): The message to display
            style (str, optional): Style to apply to the message
        """
        console.print(message, style=style)