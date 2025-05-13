from twilio_manager.shared.ui.styling import (
    clear_screen,
    print_header,
    prompt_choice,
    console
)

class BaseMenu:
    def display(self, title, emoji, options):
        """Display the menu and handle user input in a loop.
        
        Args:
            title (str): The title of the menu
            emoji (str): Emoji to display with the title
            options (dict): Dictionary mapping option keys to their descriptions
        """
        while True:
            clear_screen()
            print_header(title, emoji)
            for key, desc in options.items():
                console.print(f"[bold magenta]{key}.[/bold magenta] {desc}")
            choice = prompt_choice("Choose an option", choices=list(options.keys()), default="0")
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