"""Menu for managing configuration templates."""

import logging
from typing import Dict, Callable
from rich.table import Table
from ..base_menu import BaseMenu
from ....services.config_service import ConfigService

logger = logging.getLogger(__name__)

class ConfigMgmtMenu(BaseMenu):
    """Menu for managing configuration templates."""
    
    def __init__(self, parent: BaseMenu = None):
        """Initialize the menu.
        
        Args:
            parent: Optional parent menu for navigation.
        """
        super().__init__(parent)
        self.config_service = ConfigService()
    
    def show(self) -> None:
        """Display the configuration management menu."""
        self.clear_screen()
        self.render_header("Configuration Management")
        
        options: Dict[str, Callable] = {
            '1': self.list_templates,
            '2': self.create_template,
            '3': self.apply_template,
            '4': self.remove_template,
            '5': self.export_template,
            '6': self.import_template
        }
        
        while self.prompt_choice(options):
            self.clear_screen()
            self.render_header("Configuration Management")
    
    def list_templates(self) -> bool:
        """List configuration templates.
        
        Returns:
            True to continue menu loop.
        """
        try:
            templates = self.config_service.list_templates()
            
            if not templates:
                self.console.print("[yellow]No templates found![/yellow]")
                return True
            
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Name")
            table.add_column("Type")
            table.add_column("Created")
            table.add_column("Last Used")
            table.add_column("Description")
            
            for template in templates:
                table.add_row(
                    template.name,
                    template.type,
                    template.created_at.strftime("%Y-%m-%d"),
                    template.last_used_at.strftime("%Y-%m-%d") if template.last_used_at else "Never",
                    template.description[:50] + "..." if len(template.description) > 50 else template.description
                )
            
            self.console.print("\n[bold]Configuration Templates[/bold]")
            self.console.print(table)
            
            return True
            
        except Exception as e:
            logger.exception("Error listing templates")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def create_template(self) -> bool:
        """Create a new configuration template.
        
        Returns:
            True to continue menu loop.
        """
        try:
            name = self.prompt_input(
                "\nEnter template name: ",
                lambda x: bool(x.strip())
            )
            
            if not name:
                return True
            
            # Get template type
            types = self.config_service.get_template_types()
            
            self.console.print("\n[bold]Available Template Types:[/bold]")
            for i, type in enumerate(types, 1):
                self.console.print(f"{i}. {type}")
            
            type_choice = self.prompt_input(
                "\nSelect template type: ",
                lambda x: x.isdigit() and 1 <= int(x) <= len(types)
            )
            
            if not type_choice:
                return True
            
            template_type = types[int(type_choice) - 1]
            
            description = self.prompt_input(
                "\nEnter description (optional): "
            )
            
            # Create template
            template = self.config_service.create_template(
                name=name,
                type=template_type,
                description=description
            )
            
            self.console.print("\n[green]Template created successfully![/green]")
            self.console.print(f"Template ID: {template.id}")
            
            return True
            
        except Exception as e:
            logger.exception("Error creating template")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def apply_template(self) -> bool:
        """Apply a configuration template.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # List templates
            templates = self.config_service.list_templates()
            
            if not templates:
                self.console.print("[yellow]No templates available![/yellow]")
                return True
            
            self.console.print("\n[bold]Available Templates:[/bold]")
            for i, template in enumerate(templates, 1):
                self.console.print(f"{i}. {template.name} ({template.type})")
            
            template_choice = self.prompt_input(
                "\nSelect template number: ",
                lambda x: x.isdigit() and 1 <= int(x) <= len(templates)
            )
            
            if not template_choice:
                return True
            
            template = templates[int(template_choice) - 1]
            
            # Get target resources
            resources = self.config_service.list_eligible_resources(template.type)
            
            if not resources:
                self.console.print("[yellow]No eligible resources found![/yellow]")
                return True
            
            self.console.print("\n[bold]Select Resources:[/bold]")
            self.console.print("Enter resource numbers (comma-separated, empty for all)")
            
            for i, resource in enumerate(resources, 1):
                self.console.print(f"{i}. {resource.name} ({resource.sid})")
            
            resource_choices = self.prompt_input(
                "\nResource numbers: "
            )
            
            selected_resources = []
            if resource_choices:
                try:
                    indices = [int(x.strip()) for x in resource_choices.split(',')]
                    selected_resources = [resources[i-1] for i in indices if 1 <= i <= len(resources)]
                except (ValueError, IndexError):
                    self.console.print("[red]Invalid selection![/red]")
                    return True
            else:
                selected_resources = resources
            
            # Confirm application
            self.console.print(f"\nApplying template '{template.name}' to {len(selected_resources)} resources")
            confirm = self.prompt_input(
                "\nType 'APPLY' to confirm: ",
                lambda x: x == 'APPLY'
            )
            
            if confirm:
                self.config_service.apply_template(
                    template_id=template.id,
                    resources=selected_resources
                )
                self.console.print("\n[green]Template applied successfully![/green]")
            
            return True
            
        except Exception as e:
            logger.exception("Error applying template")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def remove_template(self) -> bool:
        """Remove a configuration template.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # List templates
            templates = self.config_service.list_templates()
            
            if not templates:
                self.console.print("[yellow]No templates available![/yellow]")
                return True
            
            self.console.print("\n[bold]Available Templates:[/bold]")
            for i, template in enumerate(templates, 1):
                self.console.print(f"{i}. {template.name} ({template.type})")
            
            template_choice = self.prompt_input(
                "\nSelect template to remove: ",
                lambda x: x.isdigit() and 1 <= int(x) <= len(templates)
            )
            
            if not template_choice:
                return True
            
            template = templates[int(template_choice) - 1]
            
            # Confirm removal
            self.console.print(f"\nRemoving template '{template.name}'")
            confirm = self.prompt_input(
                "\nType the template name to confirm: ",
                lambda x: x == template.name
            )
            
            if confirm:
                self.config_service.remove_template(template.id)
                self.console.print("\n[green]Template removed successfully![/green]")
            
            return True
            
        except Exception as e:
            logger.exception("Error removing template")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def export_template(self) -> bool:
        """Export a configuration template.
        
        Returns:
            True to continue menu loop.
        """
        try:
            # List templates
            templates = self.config_service.list_templates()
            
            if not templates:
                self.console.print("[yellow]No templates available![/yellow]")
                return True
            
            self.console.print("\n[bold]Available Templates:[/bold]")
            for i, template in enumerate(templates, 1):
                self.console.print(f"{i}. {template.name} ({template.type})")
            
            template_choice = self.prompt_input(
                "\nSelect template to export: ",
                lambda x: x.isdigit() and 1 <= int(x) <= len(templates)
            )
            
            if not template_choice:
                return True
            
            template = templates[int(template_choice) - 1]
            
            # Get filename
            filename = self.prompt_input(
                "\nEnter filename (empty for default): "
            )
            
            if not filename:
                filename = f"template_{template.name.lower().replace(' ', '_')}.json"
            
            # Export template
            self.config_service.export_template(
                template_id=template.id,
                filename=filename
            )
            
            self.console.print(f"\n[green]Template exported to {filename}![/green]")
            return True
            
        except Exception as e:
            logger.exception("Error exporting template")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def import_template(self) -> bool:
        """Import a configuration template.
        
        Returns:
            True to continue menu loop.
        """
        try:
            filename = self.prompt_input(
                "\nEnter template file path: ",
                lambda x: bool(x.strip())
            )
            
            if not filename:
                return True
            
            # Import template
            template = self.config_service.import_template(filename)
            
            self.console.print("\n[green]Template imported successfully![/green]")
            self.console.print(f"Template Name: {template.name}")
            self.console.print(f"Template ID: {template.id}")
            
            return True
            
        except Exception as e:
            logger.exception("Error importing template")
            self.console.print(f"[red]Error: {str(e)}[/red]")
            return True