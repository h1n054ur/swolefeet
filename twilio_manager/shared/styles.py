from rich.theme import Theme

class StyleConfig:
    """Centralized styling configuration for the CLI application."""
    
    # Color scheme
    PRIMARY_COLOR = "cyan"
    SECONDARY_COLOR = "magenta"
    SUCCESS_COLOR = "green"
    ERROR_COLOR = "red"
    WARNING_COLOR = "yellow"
    INFO_COLOR = "blue"
    
    # Icons
    MENU_ICONS = {
        "main": "🏠",
        "phone": "📱",
        "message": "📨",
        "voice": "📞",
        "account": "🧾",
        "advanced": "🧠",
        "back": "🔙",
        "exit": "🚪"
    }
    
    # Loading messages
    LOADING_MESSAGES = {
        "default": "Loading...",
        "saving": "Saving changes...",
        "connecting": "Connecting to Twilio...",
        "processing": "Processing request..."
    }
    
    @classmethod
    def get_theme(cls):
        """Get Rich theme with our custom styles."""
        return Theme({
            "info": f"bold {cls.INFO_COLOR}",
            "warning": f"bold {cls.WARNING_COLOR}",
            "error": f"bold {cls.ERROR_COLOR}",
            "success": f"bold {cls.SUCCESS_COLOR}",
            "primary": f"bold {cls.PRIMARY_COLOR}",
            "secondary": f"bold {cls.SECONDARY_COLOR}"
        })
    
    @classmethod
    def format_menu_title(cls, title: str, icon: str = None) -> str:
        """Format a menu title with optional icon."""
        if icon and icon in cls.MENU_ICONS:
            return f"[bold {cls.PRIMARY_COLOR}]{cls.MENU_ICONS[icon]} {title}[/bold {cls.PRIMARY_COLOR}]"
        return f"[bold {cls.PRIMARY_COLOR}]{title}[/bold {cls.PRIMARY_COLOR}]"
    
    @classmethod
    def format_menu_option(cls, number: str, text: str, icon: str = None) -> str:
        """Format a menu option with number and optional icon."""
        icon_str = f"{cls.MENU_ICONS[icon]} " if icon and icon in cls.MENU_ICONS else ""
        return f"[bold {cls.SECONDARY_COLOR}]{number}.[/bold {cls.SECONDARY_COLOR}] {icon_str}{text}"