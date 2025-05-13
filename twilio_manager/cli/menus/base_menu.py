from twilio_manager.shared.ui.styling import (
    clear_screen,
    print_header,
    prompt_choice,
    console,
    STYLES
)
from twilio_manager.shared.constants import MENU_TITLES
from twilio_manager.shared.utils.logger import get_logger

logger = get_logger(__name__)

class BaseMenu:
    def __init__(self, parent=None):
        """Initialize a menu with optional parent menu.
        
        Args:
            parent (BaseMenu, optional): Parent menu to return to
        """
        self.parent = parent

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
        logger.debug(f"Displaying menu: {title}")
        while True:
            try:
                self.clear()
                self.print_title(title, emoji)
                for key, desc in options.items():
                    console.print(f"[bold magenta]{key}.[/bold magenta] {desc}")
                choice = self.get_choice(list(options.keys()))
                if choice == "0":
                    logger.debug("User selected to return to parent menu")
                    self.return_to_parent()
                    break
                self.handle_choice(choice)
            except Exception as e:
                logger.error(f"Error in menu display loop: {str(e)}", exc_info=True)
                self.print_error("An unexpected error occurred. Please try again.")

    def handle_choice(self, choice):
        """Handle the user's menu choice. Must be implemented by subclasses.
        
        Args:
            choice (str): The user's selected option
            
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Override this method in subclasses")

    def return_to_parent(self):
        """Return to the parent menu or main menu."""
        from twilio_manager.cli.menus.main_menu import MainMenu
        logger.debug("Returning to parent menu")
        if self.parent:
            logger.debug(f"Parent menu exists: {self.parent.__class__.__name__}")
            self.parent.show()
        else:
            logger.debug("No parent menu, returning to main menu")
            MainMenu().show()

    def pause_and_return(self, message=None):
        """Display a message, pause for user input, and return to parent menu.
        
        Args:
            message (str, optional): Message to display before pausing
        """
        if message:
            self.print_info(message)
        input("\nPress Enter to return...")
        self.return_to_parent()

    def handle_empty_result(self, message="No results found."):
        """Handle empty result sets consistently.
        
        Args:
            message (str, optional): Message to display
        """
        logger.warning(f"Empty result set: {message}")
        self.print_warning(message)
        self.pause_and_return()

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
        try:
            choice = prompt_choice(prompt, choices=choices, default=default)
            logger.debug(f"User input received: {choice}")
            return choice
        except Exception as e:
            logger.error(f"Error getting user choice: {str(e)}", exc_info=True)
            return default

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
        logger.error(message)
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
        logger.warning(message)
        console.print(message, style=style)